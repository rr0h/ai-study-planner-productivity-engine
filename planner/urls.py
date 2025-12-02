from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'planner'

urlpatterns = [
    # Authentication
    path('', views.landing_page, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='planner/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Syllabus Management
    path('syllabus/upload/', views.upload_syllabus, name='upload_syllabus'),
    path('syllabus/process/<int:upload_id>/', views.process_syllabus, name='process_syllabus'),
    
    # Subject & Topic Management
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/create/', views.topic_create, name='topic_create'),
    path('topics/<int:pk>/edit/', views.topic_edit, name='topic_edit'),
    path('topics/<int:pk>/delete/', views.topic_delete, name='topic_delete'),
    
    # Schedule Management
    path('schedule/generate/', views.generate_schedule, name='generate_schedule'),
    path('schedule/calendar/', views.schedule_calendar, name='schedule_calendar'),
    path('tasks/today/', views.tasks_today, name='tasks_today'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:pk>/miss/', views.task_miss, name='task_miss'),
    
    # Revisions
    path('revisions/', views.revision_list, name='revision_list'),
    path('revisions/<int:pk>/complete/', views.revision_complete, name='revision_complete'),
    
    # Pomodoro
    path('pomodoro/', views.pomodoro_timer, name='pomodoro_timer'),
    path('pomodoro/log/', views.pomodoro_log, name='pomodoro_log'),
    path('pomodoro/sessions/', views.pomodoro_sessions, name='pomodoro_sessions'),
    
    # Questions
    path('questions/', views.question_bank, name='question_bank'),
    path('questions/generate/', views.generate_questions, name='generate_questions'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    path('analytics/data/', views.analytics_data, name='analytics_data'),
    
    # Gamification
    path('badges/', views.badges, name='badges'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
