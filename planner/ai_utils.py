"""
AI utilities for syllabus processing and question generation.
Note: This uses a mock implementation. For production, integrate with OpenAI API.
"""
import re
import random
from datetime import datetime, timedelta


def extract_topics_from_text(text):
    """
    Extract subjects, chapters, and topics from syllabus text.
    This is a simplified implementation. For production, use OpenAI API.
    """
    topics = []
    
    # Simple pattern matching for common syllabus formats
    lines = text.split('\n')
    current_subject = None
    current_chapter = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect subject (usually in caps or starts with "Subject:")
        if line.isupper() or line.lower().startswith('subject'):
            current_subject = line.replace('SUBJECT:', '').replace('Subject:', '').strip()
            continue
        
        # Detect chapter (usually starts with "Chapter" or numbers)
        if re.match(r'^(chapter|unit|module)\s+\d+', line, re.IGNORECASE):
            current_chapter = line
            continue
        
        # Detect topics (usually bullet points or numbered lists)
        if re.match(r'^[\d\.\-\*\•]\s*', line):
            topic_name = re.sub(r'^[\d\.\-\*\•]\s*', '', line).strip()
            if topic_name and current_subject:
                topics.append({
                    'subject': current_subject,
                    'chapter': current_chapter or 'General',
                    'topic': topic_name,
                    'difficulty': random.randint(3, 8),  # Mock difficulty
                    'estimated_hours': round(random.uniform(1.5, 4.0), 1)
                })
    
    # If no topics found, create some default ones
    if not topics and text:
        words = text.split()
        if len(words) > 10:
            topics.append({
                'subject': 'General Studies',
                'chapter': 'Chapter 1',
                'topic': ' '.join(words[:10]) + '...',
                'difficulty': 5,
                'estimated_hours': 2.0
            })
    
    return topics


def generate_study_schedule(topics, exam_date, daily_hours, start_date=None):
    """
    Generate a study schedule based on topics and available time.
    """
    if not start_date:
        start_date = datetime.now().date()
    
    if isinstance(exam_date, str):
        exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
    
    total_days = (exam_date - start_date).days
    if total_days <= 0:
        return []
    
    # Calculate total hours needed
    total_hours_needed = sum(topic.estimated_hours for topic in topics)
    total_hours_available = total_days * daily_hours
    
    # Reserve 20% time for revisions
    study_hours_available = total_hours_available * 0.8
    
    schedule = []
    current_date = start_date
    hours_used_today = 0
    
    for topic in topics:
        hours_needed = topic.estimated_hours
        
        while hours_needed > 0:
            if current_date >= exam_date:
                break
            
            hours_to_allocate = min(hours_needed, daily_hours - hours_used_today)
            
            if hours_to_allocate > 0:
                schedule.append({
                    'topic': topic,
                    'date': current_date,
                    'hours': hours_to_allocate
                })
                
                hours_needed -= hours_to_allocate
                hours_used_today += hours_to_allocate
            
            if hours_used_today >= daily_hours:
                current_date += timedelta(days=1)
                hours_used_today = 0
    
    return schedule


def calculate_revision_dates(completion_date):
    """
    Calculate spaced repetition revision dates.
    """
    if isinstance(completion_date, str):
        completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
    
    return {
        'day1': completion_date + timedelta(days=1),
        'day3': completion_date + timedelta(days=3),
        'day7': completion_date + timedelta(days=7),
        'day30': completion_date + timedelta(days=30),
    }


def predict_topic_difficulty(topic_name, chapter_name=''):
    """
    Predict difficulty score for a topic (1-10).
    This is a mock implementation. For production, use ML model.
    """
    # Simple heuristic based on keywords
    hard_keywords = ['advanced', 'complex', 'theorem', 'proof', 'calculus', 'quantum', 'organic']
    medium_keywords = ['analysis', 'application', 'integration', 'differentiation']
    easy_keywords = ['introduction', 'basic', 'fundamental', 'overview']
    
    text = (topic_name + ' ' + chapter_name).lower()
    
    if any(keyword in text for keyword in hard_keywords):
        return random.randint(7, 10)
    elif any(keyword in text for keyword in medium_keywords):
        return random.randint(4, 7)
    elif any(keyword in text for keyword in easy_keywords):
        return random.randint(1, 4)
    else:
        return random.randint(3, 7)


def generate_questions(topic_name, question_type, difficulty, num_questions=5):
    """
    Generate questions for a topic.
    This is a mock implementation. For production, use OpenAI API.
    """
    questions = []
    
    for i in range(num_questions):
        if question_type == 'mcq':
            question = {
                'type': 'mcq',
                'question': f"What is the key concept in {topic_name}? (Question {i+1})",
                'options': {
                    'A': f"Option A related to {topic_name}",
                    'B': f"Option B related to {topic_name}",
                    'C': f"Option C related to {topic_name}",
                    'D': f"Option D related to {topic_name}",
                },
                'correct_answer': random.choice(['A', 'B', 'C', 'D']),
                'explanation': f"This question tests understanding of {topic_name}."
            }
        elif question_type == 'short':
            question = {
                'type': 'short',
                'question': f"Briefly explain the main concept of {topic_name}. (Question {i+1})",
                'answer': f"The main concept involves understanding the fundamental principles of {topic_name}.",
                'explanation': f"A good answer should cover the key aspects of {topic_name}."
            }
        else:  # long
            question = {
                'type': 'long',
                'question': f"Discuss in detail the various aspects of {topic_name}. (Question {i+1})",
                'answer': f"A comprehensive discussion of {topic_name} should include theoretical foundations, practical applications, and real-world examples.",
                'explanation': f"This question requires in-depth knowledge of {topic_name}."
            }
        
        questions.append(question)
    
    return questions


def calculate_productivity_score(pomodoros_today, tasks_completed, revisions_done):
    """
    Calculate daily productivity score (0-100).
    """
    pomodoro_score = min(pomodoros_today * 10, 40)
    task_score = min(tasks_completed * 15, 40)
    revision_score = min(revisions_done * 20, 20)
    
    return min(pomodoro_score + task_score + revision_score, 100)


def check_badge_eligibility(user_profile, pomodoro_count, completed_topics, completed_revisions):
    """
    Check which badges the user is eligible for.
    """
    eligible_badges = []
    
    # Streak badges
    if user_profile.current_streak >= 7:
        eligible_badges.append('streak_7')
    if user_profile.current_streak >= 30:
        eligible_badges.append('streak_30')
    if user_profile.current_streak >= 100:
        eligible_badges.append('streak_100')
    
    # Pomodoro badges
    if pomodoro_count >= 100:
        eligible_badges.append('pomodoro_100')
    if pomodoro_count >= 500:
        eligible_badges.append('pomodoro_500')
    if pomodoro_count >= 1000:
        eligible_badges.append('pomodoro_1000')
    
    # Completion badges
    total_topics = user_profile.user.subjects.aggregate(
        total=models.Count('topics')
    )['total'] or 0
    
    if completed_topics == total_topics and total_topics > 0:
        eligible_badges.append('all_topics')
    
    return eligible_badges
