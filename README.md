# 🎓 AI Study Planner + Productivity Engine

A comprehensive full-stack Django web application that helps students optimize their study schedules using AI-powered syllabus analysis, smart scheduling, spaced repetition, Pomodoro tracking, and gamification.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 📚 Core Functionality

- **AI Syllabus Analysis**: Upload PDF/DOCX or paste text to automatically extract subjects, chapters, and topics
- **Smart Study Scheduling**: Generate optimized daily study plans based on exam date and available hours
- **Automatic Rescheduling**: Missed tasks are automatically moved to the next available day
- **Spaced Repetition System**: Automatic revision scheduling (Day 1, 3, 7, 30) for better retention
- **Exam Countdown**: Real-time countdown with progress tracking
- **AI Question Generator**: Generate MCQs, short, and long questions with difficulty levels
- **Topic Difficulty Prediction**: AI assigns difficulty scores (1-10) with color coding

### 🍅 Productivity Tools

- **Pomodoro Timer**: Built-in timer with 25/5 and 50/10 presets
- **Study Session Tracking**: Log and track all study sessions per topic
- **Daily Productivity Score**: Calculated based on pomodoros, tasks, and revisions

### 🎮 Gamification

- **XP System**: Earn experience points for completing tasks and revisions
- **Badge System**: Unlock achievements like "7-Day Streak", "100 Pomodoros", etc.
- **Study Streaks**: Track daily and longest study streaks
- **Leaderboard**: Compare progress with other users (optional)

### 📊 Analytics & Insights

- **Dashboard**: Beautiful overview with today's tasks, upcoming revisions, and stats
- **Analytics Page**: 
  - Weekly productivity bar charts
  - Topic completion pie charts
  - Study streak timeline
  - Subject-wise breakdown
- **Calendar View**: Visual representation of study schedule and revisions

### 🎨 Modern UI/UX

- **Tailwind CSS**: Beautiful, responsive design
- **Dark/Light Mode**: Toggle between themes
- **Glassmorphism Effects**: Modern UI panels
- **Gradient Headers**: Eye-catching visual elements
- **Hover Animations**: Smooth transitions and interactions
- **Mobile Responsive**: Works perfectly on all devices

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/rr0h/ai-study-planner-productivity-engine.git
   cd ai-study-planner-productivity-engine
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Create static files directory**
   ```bash
   mkdir static
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
ai-study-planner-productivity-engine/
├── study_planner/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── planner/                # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── views_schedule.py  # Schedule management views
│   ├── views_analytics.py # Analytics and gamification views
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin configuration
│   ├── ai_utils.py        # AI utilities
│   └── urls.py            # URL routing
├── templates/             # HTML templates
│   ├── base.html
│   └── planner/
│       ├── dashboard.html
│       ├── landing.html
│       └── ...
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploads
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## 🗄️ Database Models

- **UserProfile**: User settings, XP, streaks, exam date
- **Subject**: Study subjects with colors
- **Topic**: Individual topics with difficulty scores
- **StudyTask**: Scheduled study tasks
- **RevisionTask**: Spaced repetition revisions
- **PomodoroSession**: Pomodoro timer sessions
- **GeneratedQuestion**: AI-generated questions
- **Badge**: User achievements
- **SyllabusUpload**: Uploaded syllabus files

## 🎯 Usage Guide

### 1. Getting Started

1. Register a new account
2. Set up your profile with exam date and daily study hours
3. Upload your syllabus or manually add subjects and topics

### 2. Generate Study Schedule

1. Navigate to "Generate Schedule"
2. Select exam date, daily hours, and subjects
3. System creates optimized daily study plan

### 3. Daily Workflow

1. Check "Today's Tasks" for scheduled topics
2. Use Pomodoro timer while studying
3. Mark tasks as completed or missed
4. Complete scheduled revisions

### 4. Track Progress

1. View Dashboard for overview
2. Check Analytics for detailed insights
3. Monitor badges and achievements
4. Review calendar for upcoming tasks

## 🔧 Configuration

### AI Integration (Optional)

To enable real AI features, add OpenAI API key:

1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=your_api_key_here`
3. Update `ai_utils.py` to use OpenAI API

### Customization

- **Colors**: Edit `Subject` model color field
- **XP Values**: Modify in view functions
- **Badge Criteria**: Update in `ai_utils.py`
- **Pomodoro Durations**: Customize in templates

## 📊 Features Breakdown

### Syllabus Processing
- PDF/DOCX upload support
- Text paste option
- AI extraction of subjects, chapters, topics
- Automatic difficulty prediction

### Schedule Generation
- Considers exam date and daily hours
- Balances topics across days
- Reserves time for revisions
- Handles multiple subjects

### Revision System
- Day 1: Immediate review
- Day 3: Short-term retention
- Day 7: Weekly review
- Day 30: Long-term retention

### Gamification Elements
- **XP Rewards**:
  - Complete task: +50 XP
  - Complete revision: +30 XP
  - Complete pomodoro: +10 XP
- **Badges**:
  - Streak badges (7, 30, 100 days)
  - Pomodoro badges (100, 500, 1000)
  - Completion badges

## 🎨 UI Components

- Modal forms for quick actions
- Tab systems for organized content
- Pagination for large lists
- Loading skeletons for better UX
- Toast notifications for feedback
- Achievement popups for badges

## 📱 Responsive Design

- Mobile-first approach
- Collapsible sidebar on mobile
- Touch-friendly buttons
- Optimized layouts for all screen sizes

## 🔐 Security Features

- Django authentication system
- CSRF protection
- Password validation
- Session management
- User data isolation

## 🚧 Future Enhancements

- [ ] Google OAuth integration
- [ ] Real OpenAI API integration
- [ ] Export questions to PDF
- [ ] Mobile app (React Native)
- [ ] Collaborative study groups
- [ ] Video lecture integration
- [ ] Flashcard system
- [ ] Study music player

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ using Django and Tailwind CSS

## 🙏 Acknowledgments

- Django framework
- Tailwind CSS
- Chart.js for analytics
- Alpine.js for interactivity

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Note**: This is a local development project. No deployment configuration is included. For production deployment, additional security measures and configurations are required.
