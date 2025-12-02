from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    exam_date = models.DateField(null=True, blank=True)
    daily_study_hours = models.IntegerField(default=4)
    total_xp = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
    theme_preference = models.CharField(max_length=10, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def update_streak(self):
        today = timezone.now().date()
        if self.last_study_date:
            days_diff = (today - self.last_study_date).days
            if days_diff == 1:
                self.current_streak += 1
            elif days_diff > 1:
                self.current_streak = 1
        else:
            self.current_streak = 1
        
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.last_study_date = today
        self.save()


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Topic(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Easy-Medium'),
        (4, 'Medium'),
        (5, 'Medium'),
        (6, 'Medium-Hard'),
        (7, 'Hard'),
        (8, 'Hard'),
        (9, 'Very Hard'),
        (10, 'Extremely Hard'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    chapter = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    difficulty_score = models.IntegerField(default=5, choices=DIFFICULTY_CHOICES)
    estimated_hours = models.FloatField(default=2.0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.chapter} - {self.name}"
    
    def get_difficulty_color(self):
        if self.difficulty_score <= 3:
            return 'green'
        elif self.difficulty_score <= 6:
            return 'yellow'
        else:
            return 'red'
    
    class Meta:
        ordering = ['subject', 'chapter', 'name']


class StudyTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_tasks')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='study_tasks')
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.topic.name} - {self.scheduled_date}"
    
    class Meta:
        ordering = ['scheduled_date', 'topic']
        unique_together = ['user', 'topic', 'scheduled_date']


class RevisionTask(models.Model):
    REVISION_TYPES = [
        ('day1', 'Day 1 Revision'),
        ('day3', 'Day 3 Revision'),
        ('day7', 'Day 7 Revision'),
        ('day30', 'Day 30 Revision'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revision_tasks')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='revision_tasks')
    revision_type = models.CharField(max_length=10, choices=REVISION_TYPES)
    scheduled_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.topic.name} - {self.get_revision_type_display()} - {self.scheduled_date}"
    
    class Meta:
        ordering = ['scheduled_date', 'revision_type']


class PomodoroSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='pomodoro_sessions', null=True, blank=True)
    duration_minutes = models.IntegerField(default=25)
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.duration_minutes}min - {self.started_at.date()}"
    
    class Meta:
        ordering = ['-started_at']


class GeneratedQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('short', 'Short Answer'),
        ('long', 'Long Answer'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=500, blank=True)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_question_type_display()} - {self.topic.name}"
    
    class Meta:
        ordering = ['-created_at']


class Badge(models.Model):
    BADGE_TYPES = [
        ('streak_7', '7-Day Streak'),
        ('streak_30', '30-Day Streak'),
        ('streak_100', '100-Day Streak'),
        ('pomodoro_100', '100 Pomodoros'),
        ('pomodoro_500', '500 Pomodoros'),
        ('pomodoro_1000', '1000 Pomodoros'),
        ('all_revisions', 'All Revisions Done'),
        ('all_topics', 'All Topics Completed'),
        ('early_bird', 'Early Bird'),
        ('night_owl', 'Night Owl'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_badge_type_display()}"
    
    class Meta:
        ordering = ['-earned_at']
        unique_together = ['user', 'badge_type']


class SyllabusUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='syllabus_uploads')
    file = models.FileField(upload_to='syllabi/')
    text_content = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at.date()}"
    
    class Meta:
        ordering = ['-uploaded_at']
