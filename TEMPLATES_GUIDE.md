# Templates Guide

This document provides a guide for creating the remaining templates. All templates should extend `base.html` and follow the Tailwind CSS design system.

## Required Templates

### 1. Profile Management
- `templates/planner/profile.html` - User profile settings

### 2. Syllabus Management
- `templates/planner/upload_syllabus.html` - Upload syllabus form

### 3. Subject Management
- `templates/planner/subject_list.html` - List all subjects
- `templates/planner/subject_form.html` - Create/edit subject
- `templates/planner/subject_confirm_delete.html` - Delete confirmation

### 4. Topic Management
- `templates/planner/topic_list.html` - List all topics
- `templates/planner/topic_form.html` - Create/edit topic
- `templates/planner/topic_confirm_delete.html` - Delete confirmation

### 5. Schedule Management
- `templates/planner/generate_schedule.html` - Schedule generation form
- `templates/planner/schedule_calendar.html` - Calendar view
- `templates/planner/tasks_today.html` - Today's tasks
- `templates/planner/task_update.html` - Update task status

### 6. Revision Management
- `templates/planner/revision_list.html` - List revisions

### 7. Pomodoro Timer
- `templates/planner/pomodoro_timer.html` - Timer interface
- `templates/planner/pomodoro_sessions.html` - Session history

### 8. Question Bank
- `templates/planner/question_bank.html` - Question list with filters
- `templates/planner/generate_questions.html` - Question generation form
- `templates/planner/question_detail.html` - Question details

### 9. Analytics
- `templates/planner/analytics.html` - Analytics dashboard

### 10. Gamification
- `templates/planner/badges.html` - Badges and achievements
- `templates/planner/leaderboard.html` - User leaderboard

## Template Structure

Each template should follow this structure:

```django
{% extends 'base.html' %}

{% block title %}Page Title - AI Study Planner{% endblock %}
{% block page_title %}Page Title{% endblock %}

{% block content %}
<!-- Page content here -->
{% endblock %}

{% block extra_js %}
<!-- Page-specific JavaScript -->
{% endblock %}
```

## Design Guidelines

1. **Colors**: Use Tailwind's color palette with purple/blue gradients for primary actions
2. **Cards**: Use `rounded-xl shadow-lg` for card components
3. **Buttons**: Primary buttons should use gradient backgrounds
4. **Forms**: Use consistent form styling with labels and error messages
5. **Icons**: Use Heroicons (included via Tailwind)
6. **Responsive**: All layouts should be mobile-responsive
7. **Dark Mode**: Support dark mode with `dark:` classes

## Quick Template Creation

For rapid development, you can create minimal templates that will be functional:

### Minimal Template Example:
```django
{% extends 'base.html' %}
{% block title %}Page Name{% endblock %}
{% block page_title %}Page Name{% endblock %}
{% block content %}
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
    <h2 class="text-2xl font-bold mb-4">Content Title</h2>
    <!-- Add your content here -->
</div>
{% endblock %}
```

## Creating Templates Manually

If you need to create templates manually after cloning:

1. Navigate to `templates/planner/` directory
2. Create HTML files following the naming convention
3. Use the base template structure above
4. Add your specific content
5. Test in the browser

## Template Variables

Common variables available in templates:
- `user` - Current authenticated user
- `user.profile` - User profile with XP, streaks, etc.
- `messages` - Django messages framework
- Context-specific variables passed from views

## Forms in Templates

When rendering Django forms:
```django
<form method="post" class="space-y-4">
    {% csrf_token %}
    {% for field in form %}
        <div>
            <label class="block text-sm font-medium mb-1">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
                <p class="text-red-600 text-sm mt-1">{{ field.errors.0 }}</p>
            {% endif %}
        </div>
    {% endfor %}
    <button type="submit" class="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-lg">
        Submit
    </button>
</form>
```

## Next Steps

After setting up the project:
1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Start server: `python manage.py runserver`
4. Create remaining templates as needed
5. Test all functionality

The application will work with minimal templates - you can create beautiful, detailed templates incrementally as you use the application.
