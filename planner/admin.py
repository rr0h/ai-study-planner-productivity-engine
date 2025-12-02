from django.contrib import admin
from .models import (
    UserProfile, Subject, Topic, StudyTask, 
    RevisionTask, PomodoroSession, GeneratedQuestion, 
    Badge, SyllabusUpload
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam_date', 'daily_study_hours', 'total_xp', 'current_streak']
    search_fields = ['user__username', 'user__email']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'chapter', 'subject', 'difficulty_score', 'is_completed']
    list_filter = ['subject', 'difficulty_score', 'is_completed']
    search_fields = ['name', 'chapter']


@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'scheduled_date', 'status']
    list_filter = ['status', 'scheduled_date', 'user']
    search_fields = ['topic__name', 'user__username']


@admin.register(RevisionTask)
class RevisionTaskAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'revision_type', 'scheduled_date', 'is_completed']
    list_filter = ['revision_type', 'is_completed', 'scheduled_date']
    search_fields = ['topic__name', 'user__username']


@admin.register(PomodoroSession)
class PomodoroSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'duration_minutes', 'started_at', 'completed']
    list_filter = ['completed', 'duration_minutes', 'started_at']
    search_fields = ['user__username', 'topic__name']


@admin.register(GeneratedQuestion)
class GeneratedQuestionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'question_type', 'difficulty', 'created_at']
    list_filter = ['question_type', 'difficulty', 'created_at']
    search_fields = ['question_text', 'topic__name']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge_type', 'earned_at']
    list_filter = ['badge_type', 'earned_at']
    search_fields = ['user__username']


@admin.register(SyllabusUpload)
class SyllabusUploadAdmin(admin.ModelAdmin):
    list_display = ['user', 'uploaded_at', 'processed']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['user__username']
