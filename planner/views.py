from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    UserProfile, Subject, Topic, StudyTask, RevisionTask,
    PomodoroSession, GeneratedQuestion, Badge, SyllabusUpload
)
from .forms import (
    UserRegistrationForm, UserProfileForm, SubjectForm, TopicForm,
    SyllabusUploadForm, ScheduleGeneratorForm, QuestionGeneratorForm
)
from .ai_utils import (
    extract_topics_from_text, generate_study_schedule, calculate_revision_dates,
    predict_topic_difficulty, generate_questions as ai_generate_questions, 
    calculate_productivity_score, check_badge_eligibility
)


# Authentication Views
def landing_page(request):
    """Landing page for non-authenticated users."""
    if request.user.is_authenticated:
        return redirect('planner:dashboard')
    return render(request, 'planner/landing.html')


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AI Study Planner.')
            return redirect('planner:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'planner/register.html', {'form': form})


# Dashboard Views
@login_required
def dashboard(request):
    """Main dashboard view."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get today's tasks
    today = timezone.now().date()
    today_tasks = StudyTask.objects.filter(
        user=request.user,
        scheduled_date=today
    ).select_related('topic', 'topic__subject')
    
    # Get upcoming revisions
    upcoming_revisions = RevisionTask.objects.filter(
        user=request.user,
        is_completed=False,
        scheduled_date__gte=today
    ).select_related('topic', 'topic__subject').order_by('scheduled_date')[:5]
    
    # Get today's pomodoros
    today_pomodoros = PomodoroSession.objects.filter(
        user=request.user,
        started_at__date=today,
        completed=True
    ).count()
    
    # Calculate stats
    total_topics = Topic.objects.filter(subject__user=request.user).count()
    completed_topics = Topic.objects.filter(
        subject__user=request.user,
        is_completed=True
    ).count()
    
    completion_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0
    
    # Exam countdown
    days_until_exam = None
    if profile.exam_date:
        days_until_exam = (profile.exam_date - today).days
    
    # Calculate productivity score
    tasks_completed_today = today_tasks.filter(status='completed').count()
    revisions_done_today = RevisionTask.objects.filter(
        user=request.user,
        completed_at__date=today
    ).count()
    
    productivity_score = calculate_productivity_score(
        today_pomodoros,
        tasks_completed_today,
        revisions_done_today
    )
    
    context = {
        'profile': profile,
        'today_tasks': today_tasks,
        'upcoming_revisions': upcoming_revisions,
        'today_pomodoros': today_pomodoros,
        'total_topics': total_topics,
        'completed_topics': completed_topics,
        'completion_percentage': round(completion_percentage, 1),
        'days_until_exam': days_until_exam,
        'productivity_score': productivity_score,
    }
    
    return render(request, 'planner/dashboard.html', context)


@login_required
def profile(request):
    """User profile management."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('planner:dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'planner/profile.html', {'form': form, 'profile': profile})


# Syllabus Management Views
@login_required
def upload_syllabus(request):
    """Upload and process syllabus."""
    if request.method == 'POST':
        form = SyllabusUploadForm(request.POST, request.FILES)
        if form.is_valid():
            syllabus = form.save(commit=False)
            syllabus.user = request.user
            
            # Handle text input
            if form.cleaned_data.get('text_input'):
                syllabus.text_content = form.cleaned_data['text_input']
            
            syllabus.save()
            messages.success(request, 'Syllabus uploaded successfully!')
            return redirect('planner:process_syllabus', upload_id=syllabus.id)
    else:
        form = SyllabusUploadForm()
    
    return render(request, 'planner/upload_syllabus.html', {'form': form})


@login_required
def process_syllabus(request, upload_id):
    """Process uploaded syllabus and extract topics."""
    syllabus = get_object_or_404(SyllabusUpload, id=upload_id, user=request.user)
    
    if not syllabus.processed:
        # Extract text from file if needed
        text_content = syllabus.text_content
        
        if syllabus.file and not text_content:
            # Simple text extraction (for production, use proper PDF/DOCX parsers)
            try:
                if syllabus.file.name.endswith('.txt'):
                    text_content = syllabus.file.read().decode('utf-8')
                else:
                    text_content = "Sample syllabus content for processing"
            except Exception as e:
                messages.error(request, f'Error reading file: {str(e)}')
                return redirect('planner:upload_syllabus')
        
        # Extract topics using AI
        extracted_topics = extract_topics_from_text(text_content)
        
        # Create subjects and topics
        for item in extracted_topics:
            subject, _ = Subject.objects.get_or_create(
                user=request.user,
                name=item['subject']
            )
            
            Topic.objects.create(
                subject=subject,
                chapter=item['chapter'],
                name=item['topic'],
                difficulty_score=item['difficulty'],
                estimated_hours=item['estimated_hours']
            )
        
        syllabus.processed = True
        syllabus.save()
        
        messages.success(request, f'Successfully extracted {len(extracted_topics)} topics!')
    
    return redirect('planner:topic_list')


# Subject Management Views
@login_required
def subject_list(request):
    """List all subjects."""
    subjects = Subject.objects.filter(user=request.user).annotate(
        topic_count=Count('topics'),
        completed_count=Count('topics', filter=Q(topics__is_completed=True))
    )
    return render(request, 'planner/subject_list.html', {'subjects': subjects})


@login_required
def subject_create(request):
    """Create new subject."""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('planner:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'planner/subject_form.html', {'form': form, 'action': 'Create'})


@login_required
def subject_edit(request, pk):
    """Edit existing subject."""
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('planner:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'planner/subject_form.html', {'form': form, 'action': 'Edit'})


@login_required
def subject_delete(request, pk):
    """Delete subject."""
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('planner:subject_list')
    return render(request, 'planner/subject_confirm_delete.html', {'subject': subject})


# Topic Management Views
@login_required
def topic_list(request):
    """List all topics."""
    topics = Topic.objects.filter(subject__user=request.user).select_related('subject')
    return render(request, 'planner/topic_list.html', {'topics': topics})


@login_required
def topic_create(request):
    """Create new topic."""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('planner:topic_list')
    else:
        form = TopicForm()
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
    return render(request, 'planner/topic_form.html', {'form': form, 'action': 'Create'})


@login_required
def topic_edit(request, pk):
    """Edit existing topic."""
    topic = get_object_or_404(Topic, pk=pk, subject__user=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated successfully!')
            return redirect('planner:topic_list')
    else:
        form = TopicForm(instance=topic)
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
    return render(request, 'planner/topic_form.html', {'form': form, 'action': 'Edit'})


@login_required
def topic_delete(request, pk):
    """Delete topic."""
    topic = get_object_or_404(Topic, pk=pk, subject__user=request.user)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Topic deleted successfully!')
        return redirect('planner:topic_list')
    return render(request, 'planner/topic_confirm_delete.html', {'topic': topic})


# Import additional views from separate modules
from .views_schedule import (
    generate_schedule, schedule_calendar, tasks_today, task_update,
    task_complete, task_miss, revision_list, revision_complete,
    pomodoro_timer, pomodoro_log, pomodoro_sessions
)

from .views_analytics import (
    question_bank, generate_questions, question_detail,
    analytics, analytics_data, badges, leaderboard
)
