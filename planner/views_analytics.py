"""
Analytics, questions, and gamification views.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    UserProfile, Subject, Topic, StudyTask, RevisionTask,
    PomodoroSession, GeneratedQuestion, Badge
)
from .forms import QuestionGeneratorForm
from .ai_utils import generate_questions as ai_generate_questions


@login_required
def question_bank(request):
    """Display question bank with filters."""
    questions = GeneratedQuestion.objects.filter(
        topic__subject__user=request.user
    ).select_related('topic', 'topic__subject')
    
    # Apply filters
    subject_id = request.GET.get('subject')
    question_type = request.GET.get('type')
    difficulty = request.GET.get('difficulty')
    
    if subject_id:
        questions = questions.filter(topic__subject_id=subject_id)
    if question_type:
        questions = questions.filter(question_type=question_type)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    
    subjects = Subject.objects.filter(user=request.user)
    
    context = {
        'questions': questions,
        'subjects': subjects,
        'selected_subject': subject_id,
        'selected_type': question_type,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'planner/question_bank.html', context)


@login_required
def generate_questions(request):
    """Generate AI questions for a topic."""
    if request.method == 'POST':
        form = QuestionGeneratorForm(request.user, request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            question_type = form.cleaned_data['question_type']
            difficulty = form.cleaned_data['difficulty']
            num_questions = form.cleaned_data['num_questions']
            
            # Generate questions using AI
            generated = ai_generate_questions(
                topic.name,
                question_type,
                difficulty,
                num_questions
            )
            
            # Save to database
            for q in generated:
                if q['type'] == 'mcq':
                    GeneratedQuestion.objects.create(
                        topic=topic,
                        question_type='mcq',
                        difficulty=difficulty,
                        question_text=q['question'],
                        option_a=q['options']['A'],
                        option_b=q['options']['B'],
                        option_c=q['options']['C'],
                        option_d=q['options']['D'],
                        correct_answer=q['correct_answer'],
                        explanation=q['explanation']
                    )
                else:
                    GeneratedQuestion.objects.create(
                        topic=topic,
                        question_type=question_type,
                        difficulty=difficulty,
                        question_text=q['question'],
                        correct_answer=q.get('answer', ''),
                        explanation=q['explanation']
                    )
            
            messages.success(request, f'Generated {num_questions} questions successfully!')
            return redirect('planner:question_bank')
    else:
        form = QuestionGeneratorForm(request.user)
    
    return render(request, 'planner/generate_questions.html', {'form': form})


@login_required
def question_detail(request, pk):
    """Display question details."""
    question = get_object_or_404(
        GeneratedQuestion,
        pk=pk,
        topic__subject__user=request.user
    )
    return render(request, 'planner/question_detail.html', {'question': question})


@login_required
def analytics(request):
    """Analytics dashboard."""
    profile = request.user.profile
    today = timezone.now().date()
    
    # Weekly productivity data
    week_data = []
    for i in range(7):
        date = today - timedelta(days=6-i)
        pomodoros = PomodoroSession.objects.filter(
            user=request.user,
            started_at__date=date,
            completed=True
        ).count()
        
        tasks = StudyTask.objects.filter(
            user=request.user,
            completed_at__date=date
        ).count()
        
        week_data.append({
            'date': date.strftime('%a'),
            'pomodoros': pomodoros,
            'tasks': tasks
        })
    
    # Topic completion stats
    total_topics = Topic.objects.filter(subject__user=request.user).count()
    completed_topics = Topic.objects.filter(
        subject__user=request.user,
        is_completed=True
    ).count()
    pending_topics = total_topics - completed_topics
    
    # Subject-wise breakdown
    subject_stats = []
    subjects = Subject.objects.filter(user=request.user).annotate(
        total=Count('topics'),
        completed=Count('topics', filter=Q(topics__is_completed=True))
    )
    
    for subject in subjects:
        subject_stats.append({
            'name': subject.name,
            'total': subject.total,
            'completed': subject.completed,
            'pending': subject.total - subject.completed,
            'percentage': round((subject.completed / subject.total * 100) if subject.total > 0 else 0, 1)
        })
    
    # Streak data
    streak_data = []
    for i in range(30):
        date = today - timedelta(days=29-i)
        has_activity = PomodoroSession.objects.filter(
            user=request.user,
            started_at__date=date,
            completed=True
        ).exists() or StudyTask.objects.filter(
            user=request.user,
            completed_at__date=date
        ).exists()
        
        streak_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'active': has_activity
        })
    
    # Revision stats
    total_revisions = RevisionTask.objects.filter(user=request.user).count()
    completed_revisions = RevisionTask.objects.filter(
        user=request.user,
        is_completed=True
    ).count()
    
    context = {
        'profile': profile,
        'week_data': json.dumps(week_data),
        'total_topics': total_topics,
        'completed_topics': completed_topics,
        'pending_topics': pending_topics,
        'subject_stats': subject_stats,
        'streak_data': json.dumps(streak_data),
        'total_revisions': total_revisions,
        'completed_revisions': completed_revisions,
    }
    
    return render(request, 'planner/analytics.html', context)


@login_required
def analytics_data(request):
    """API endpoint for analytics data."""
    today = timezone.now().date()
    
    # Get date range
    days = int(request.GET.get('days', 7))
    start_date = today - timedelta(days=days-1)
    
    # Collect data
    data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        
        pomodoros = PomodoroSession.objects.filter(
            user=request.user,
            started_at__date=date,
            completed=True
        ).count()
        
        tasks = StudyTask.objects.filter(
            user=request.user,
            completed_at__date=date
        ).count()
        
        revisions = RevisionTask.objects.filter(
            user=request.user,
            completed_at__date=date
        ).count()
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'pomodoros': pomodoros,
            'tasks': tasks,
            'revisions': revisions
        })
    
    return JsonResponse({'data': data})


@login_required
def badges(request):
    """Display user badges and achievements."""
    user_badges = Badge.objects.filter(user=request.user).order_by('-earned_at')
    
    # Calculate stats for potential badges
    total_pomodoros = PomodoroSession.objects.filter(
        user=request.user,
        completed=True
    ).count()
    
    completed_topics = Topic.objects.filter(
        subject__user=request.user,
        is_completed=True
    ).count()
    
    total_topics = Topic.objects.filter(subject__user=request.user).count()
    
    completed_revisions = RevisionTask.objects.filter(
        user=request.user,
        is_completed=True
    ).count()
    
    profile = request.user.profile
    
    # Define all possible badges with progress
    all_badges = [
        {
            'type': 'streak_7',
            'name': '7-Day Streak',
            'description': 'Study for 7 consecutive days',
            'icon': '🔥',
            'earned': user_badges.filter(badge_type='streak_7').exists(),
            'progress': min(profile.current_streak, 7),
            'target': 7
        },
        {
            'type': 'streak_30',
            'name': '30-Day Streak',
            'description': 'Study for 30 consecutive days',
            'icon': '🔥🔥',
            'earned': user_badges.filter(badge_type='streak_30').exists(),
            'progress': min(profile.current_streak, 30),
            'target': 30
        },
        {
            'type': 'pomodoro_100',
            'name': '100 Pomodoros',
            'description': 'Complete 100 pomodoro sessions',
            'icon': '🍅',
            'earned': user_badges.filter(badge_type='pomodoro_100').exists(),
            'progress': min(total_pomodoros, 100),
            'target': 100
        },
        {
            'type': 'pomodoro_500',
            'name': '500 Pomodoros',
            'description': 'Complete 500 pomodoro sessions',
            'icon': '🍅🍅',
            'earned': user_badges.filter(badge_type='pomodoro_500').exists(),
            'progress': min(total_pomodoros, 500),
            'target': 500
        },
        {
            'type': 'all_topics',
            'name': 'All Topics Completed',
            'description': 'Complete all topics in your syllabus',
            'icon': '🎓',
            'earned': user_badges.filter(badge_type='all_topics').exists(),
            'progress': completed_topics,
            'target': total_topics if total_topics > 0 else 1
        },
        {
            'type': 'all_revisions',
            'name': 'All Revisions Done',
            'description': 'Complete all scheduled revisions',
            'icon': '📚',
            'earned': user_badges.filter(badge_type='all_revisions').exists(),
            'progress': completed_revisions,
            'target': max(completed_revisions, 1)
        },
    ]
    
    context = {
        'all_badges': all_badges,
        'earned_count': user_badges.count(),
        'total_xp': profile.total_xp,
        'current_streak': profile.current_streak,
        'longest_streak': profile.longest_streak,
    }
    
    return render(request, 'planner/badges.html', context)


@login_required
def leaderboard(request):
    """Display leaderboard (optional feature)."""
    top_users = UserProfile.objects.select_related('user').order_by('-total_xp')[:10]
    
    # Get current user rank
    user_rank = UserProfile.objects.filter(
        total_xp__gt=request.user.profile.total_xp
    ).count() + 1
    
    context = {
        'top_users': top_users,
        'user_rank': user_rank,
        'user_profile': request.user.profile,
    }
    
    return render(request, 'planner/leaderboard.html', context)
