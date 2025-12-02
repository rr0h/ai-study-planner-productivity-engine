"""
Schedule and task management views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    UserProfile, Subject, Topic, StudyTask, RevisionTask,
    PomodoroSession, GeneratedQuestion, Badge
)
from .forms import ScheduleGeneratorForm, QuestionGeneratorForm
from .ai_utils import (
    generate_study_schedule, calculate_revision_dates,
    generate_questions as ai_generate_questions,
    check_badge_eligibility
)


@login_required
def generate_schedule(request):
    """Generate study schedule based on topics and exam date."""
    if request.method == 'POST':
        form = ScheduleGeneratorForm(request.user, request.POST)
        if form.is_valid():
            exam_date = form.cleaned_data['exam_date']
            daily_hours = form.cleaned_data['daily_hours']
            subjects = form.cleaned_data['subjects']
            
            # Get all topics for selected subjects
            topics = Topic.objects.filter(
                subject__in=subjects,
                is_completed=False
            ).order_by('difficulty_score')
            
            # Generate schedule
            schedule = generate_study_schedule(
                topics,
                exam_date,
                daily_hours
            )
            
            # Create study tasks
            created_count = 0
            for item in schedule:
                StudyTask.objects.get_or_create(
                    user=request.user,
                    topic=item['topic'],
                    scheduled_date=item['date'],
                    defaults={'status': 'pending'}
                )
                created_count += 1
            
            # Update user profile
            profile = request.user.profile
            profile.exam_date = exam_date
            profile.daily_study_hours = daily_hours
            profile.save()
            
            messages.success(request, f'Schedule generated! Created {created_count} study tasks.')
            return redirect('planner:schedule_calendar')
    else:
        form = ScheduleGeneratorForm(request.user)
    
    return render(request, 'planner/generate_schedule.html', {'form': form})


@login_required
def schedule_calendar(request):
    """Display study schedule in calendar view."""
    # Get date range
    today = timezone.now().date()
    start_date = today - timedelta(days=7)
    end_date = today + timedelta(days=30)
    
    # Get tasks
    tasks = StudyTask.objects.filter(
        user=request.user,
        scheduled_date__range=[start_date, end_date]
    ).select_related('topic', 'topic__subject').order_by('scheduled_date')
    
    # Get revisions
    revisions = RevisionTask.objects.filter(
        user=request.user,
        scheduled_date__range=[start_date, end_date]
    ).select_related('topic', 'topic__subject').order_by('scheduled_date')
    
    # Organize by date
    calendar_data = {}
    current = start_date
    while current <= end_date:
        calendar_data[current] = {
            'tasks': [],
            'revisions': []
        }
        current += timedelta(days=1)
    
    for task in tasks:
        if task.scheduled_date in calendar_data:
            calendar_data[task.scheduled_date]['tasks'].append(task)
    
    for revision in revisions:
        if revision.scheduled_date in calendar_data:
            calendar_data[revision.scheduled_date]['revisions'].append(revision)
    
    context = {
        'calendar_data': calendar_data,
        'today': today,
    }
    
    return render(request, 'planner/schedule_calendar.html', context)


@login_required
def tasks_today(request):
    """Display today's tasks."""
    today = timezone.now().date()
    tasks = StudyTask.objects.filter(
        user=request.user,
        scheduled_date=today
    ).select_related('topic', 'topic__subject')
    
    return render(request, 'planner/tasks_today.html', {'tasks': tasks, 'today': today})


@login_required
def task_update(request, pk):
    """Update task status."""
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        task.status = status
        task.notes = notes
        
        if status == 'completed':
            task.completed_at = timezone.now()
            task.topic.is_completed = True
            task.topic.completed_at = timezone.now()
            task.topic.save()
            
            # Create revision tasks
            revision_dates = calculate_revision_dates(task.completed_at.date())
            for rev_type, rev_date in revision_dates.items():
                RevisionTask.objects.get_or_create(
                    user=request.user,
                    topic=task.topic,
                    revision_type=rev_type,
                    scheduled_date=rev_date
                )
            
            # Award XP
            profile = request.user.profile
            profile.total_xp += 50
            profile.update_streak()
            profile.save()
            
            messages.success(request, f'Task completed! +50 XP. Revision tasks created.')
        
        task.save()
        return redirect('planner:tasks_today')
    
    return render(request, 'planner/task_update.html', {'task': task})


@login_required
def task_complete(request, pk):
    """Mark task as completed."""
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    
    task.status = 'completed'
    task.completed_at = timezone.now()
    task.save()
    
    # Mark topic as completed
    task.topic.is_completed = True
    task.topic.completed_at = timezone.now()
    task.topic.save()
    
    # Create revision tasks
    revision_dates = calculate_revision_dates(task.completed_at.date())
    for rev_type, rev_date in revision_dates.items():
        RevisionTask.objects.get_or_create(
            user=request.user,
            topic=task.topic,
            revision_type=rev_type,
            scheduled_date=rev_date
        )
    
    # Award XP
    profile = request.user.profile
    profile.total_xp += 50
    profile.update_streak()
    profile.save()
    
    messages.success(request, 'Task completed! +50 XP')
    return redirect('planner:tasks_today')


@login_required
def task_miss(request, pk):
    """Mark task as missed and reschedule."""
    task = get_object_or_404(StudyTask, pk=pk, user=request.user)
    
    task.status = 'missed'
    task.save()
    
    # Reschedule to next available day
    next_date = task.scheduled_date + timedelta(days=1)
    
    # Find next available slot
    while StudyTask.objects.filter(
        user=request.user,
        scheduled_date=next_date
    ).count() >= 5:  # Max 5 tasks per day
        next_date += timedelta(days=1)
    
    # Create new task
    StudyTask.objects.create(
        user=request.user,
        topic=task.topic,
        scheduled_date=next_date,
        status='pending'
    )
    
    messages.info(request, f'Task rescheduled to {next_date}')
    return redirect('planner:tasks_today')


@login_required
def revision_list(request):
    """List all revision tasks."""
    today = timezone.now().date()
    
    pending_revisions = RevisionTask.objects.filter(
        user=request.user,
        is_completed=False,
        scheduled_date__lte=today + timedelta(days=7)
    ).select_related('topic', 'topic__subject').order_by('scheduled_date')
    
    completed_revisions = RevisionTask.objects.filter(
        user=request.user,
        is_completed=True
    ).select_related('topic', 'topic__subject').order_by('-completed_at')[:20]
    
    context = {
        'pending_revisions': pending_revisions,
        'completed_revisions': completed_revisions,
    }
    
    return render(request, 'planner/revision_list.html', context)


@login_required
def revision_complete(request, pk):
    """Mark revision as completed."""
    revision = get_object_or_404(RevisionTask, pk=pk, user=request.user)
    
    revision.is_completed = True
    revision.completed_at = timezone.now()
    revision.save()
    
    # Award XP
    profile = request.user.profile
    profile.total_xp += 30
    profile.save()
    
    messages.success(request, 'Revision completed! +30 XP')
    return redirect('planner:revision_list')


@login_required
def pomodoro_timer(request):
    """Pomodoro timer page."""
    topics = Topic.objects.filter(
        subject__user=request.user,
        is_completed=False
    ).select_related('subject')
    
    return render(request, 'planner/pomodoro_timer.html', {'topics': topics})


@login_required
def pomodoro_log(request):
    """Log a completed pomodoro session."""
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        duration = int(request.POST.get('duration', 25))
        
        topic = None
        if topic_id:
            topic = get_object_or_404(Topic, pk=topic_id, subject__user=request.user)
        
        session = PomodoroSession.objects.create(
            user=request.user,
            topic=topic,
            duration_minutes=duration,
            completed=True
        )
        
        # Award XP
        profile = request.user.profile
        profile.total_xp += 10
        profile.save()
        
        # Check for pomodoro badges
        total_pomodoros = PomodoroSession.objects.filter(
            user=request.user,
            completed=True
        ).count()
        
        if total_pomodoros == 100:
            Badge.objects.get_or_create(user=request.user, badge_type='pomodoro_100')
            messages.success(request, '🎉 Badge Unlocked: 100 Pomodoros!')
        elif total_pomodoros == 500:
            Badge.objects.get_or_create(user=request.user, badge_type='pomodoro_500')
            messages.success(request, '🎉 Badge Unlocked: 500 Pomodoros!')
        
        return JsonResponse({
            'success': True,
            'xp_earned': 10,
            'total_pomodoros': total_pomodoros
        })
    
    return JsonResponse({'success': False})


@login_required
def pomodoro_sessions(request):
    """View pomodoro session history."""
    sessions = PomodoroSession.objects.filter(
        user=request.user
    ).select_related('topic', 'topic__subject').order_by('-started_at')[:50]
    
    # Calculate stats
    today = timezone.now().date()
    today_sessions = sessions.filter(started_at__date=today, completed=True).count()
    week_sessions = sessions.filter(
        started_at__date__gte=today - timedelta(days=7),
        completed=True
    ).count()
    
    context = {
        'sessions': sessions,
        'today_sessions': today_sessions,
        'week_sessions': week_sessions,
    }
    
    return render(request, 'planner/pomodoro_sessions.html', context)
