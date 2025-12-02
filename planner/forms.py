from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Subject, Topic, SyllabusUpload


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['exam_date', 'daily_study_hours', 'theme_preference']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'daily_study_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '24'}),
            'theme_preference': forms.Select(attrs={'class': 'form-select'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Mathematics'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-input'}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'chapter', 'name', 'difficulty_score', 'estimated_hours']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'chapter': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Chapter 1: Algebra'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Linear Equations'}),
            'difficulty_score': forms.Select(attrs={'class': 'form-select'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5', 'min': '0.5'}),
        }


class SyllabusUploadForm(forms.ModelForm):
    text_input = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Or paste your syllabus text here...',
            'rows': 10
        })
    )
    
    class Meta:
        model = SyllabusUpload
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-input', 'accept': '.pdf,.docx,.txt'}),
        }


class ScheduleGeneratorForm(forms.Form):
    exam_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        label='Exam Date'
    )
    daily_hours = forms.IntegerField(
        min_value=1,
        max_value=24,
        widget=forms.NumberInput(attrs={'class': 'form-input'}),
        label='Daily Study Hours'
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        label='Select Subjects'
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.filter(user=user)


class QuestionGeneratorForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice Questions'),
        ('short', 'Short Answer Questions'),
        ('long', 'Long Answer Questions'),
    ]
    
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select Topic'
    )
    question_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Question Type'
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Difficulty Level'
    )
    num_questions = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-input'}),
        label='Number of Questions'
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(subject__user=user)
