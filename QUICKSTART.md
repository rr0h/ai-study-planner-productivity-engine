# 🚀 Quick Start Guide - AI Study Planner

Get up and running in **5 minutes**!

## ⚡ Super Quick Setup (Automated)

### Option 1: Linux/Mac
```bash
git clone https://github.com/rr0h/ai-study-planner-productivity-engine.git
cd ai-study-planner-productivity-engine
chmod +x setup.sh
./setup.sh
```

### Option 2: Windows
```bash
git clone https://github.com/rr0h/ai-study-planner-productivity-engine.git
cd ai-study-planner-productivity-engine
setup.bat
```

The setup script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Run database migrations
- ✅ Prompt for superuser creation (optional)

---

## 📝 Manual Setup (Step by Step)

### 1. Clone Repository
```bash
git clone https://github.com/rr0h/ai-study-planner-productivity-engine.git
cd ai-study-planner-productivity-engine
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Directories
```bash
# Windows
mkdir static
mkdir media

# Linux/Mac
mkdir -p static media
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 7. Start Server
```bash
python manage.py runserver
```

### 8. Access Application
Open your browser and go to:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🎯 First Time Usage

### Step 1: Register Account
1. Go to http://127.0.0.1:8000/
2. Click "Get Started" or "Register"
3. Fill in username, email, password
4. Click "Register"

### Step 2: Set Up Profile
1. You'll be redirected to profile page
2. Set your **Exam Date**
3. Set **Daily Study Hours** (e.g., 4 hours)
4. Choose theme preference
5. Click "Save Changes"

### Step 3: Add Your Syllabus

**Option A: Paste Text**
1. Go to "Upload Syllabus"
2. Paste your syllabus in the text area
3. Click "Process Syllabus"

**Option B: Upload File**
1. Go to "Upload Syllabus"
2. Choose PDF/DOCX/TXT file
3. Click "Process Syllabus"

**Sample Syllabus Text:**
```
MATHEMATICS

Chapter 1: Algebra
- Linear Equations
- Quadratic Equations
- Polynomials
- Factorization

Chapter 2: Calculus
- Differentiation
- Integration
- Limits and Continuity

PHYSICS

Chapter 1: Mechanics
- Newton's Laws of Motion
- Work, Energy and Power
- Momentum and Collisions

Chapter 2: Thermodynamics
- Laws of Thermodynamics
- Heat Transfer
- Entropy
```

### Step 4: Generate Schedule
1. Go to "Generate Schedule"
2. Select exam date
3. Choose daily study hours
4. Select subjects to include
5. Click "Generate Schedule"

### Step 5: Start Studying!
1. Check "Today's Tasks" for what to study
2. Use "Pomodoro Timer" while studying
3. Mark tasks as completed
4. Track your progress in "Analytics"
5. Earn badges and XP!

---

## 🎮 Key Features to Try

### 1. Dashboard
- View today's tasks
- See upcoming revisions
- Check productivity score
- Monitor exam countdown

### 2. Pomodoro Timer
- Choose 25-min or 50-min sessions
- Select topic (optional)
- Start timer and study
- Earn +10 XP per session

### 3. Task Management
- View today's tasks
- Mark as completed (+50 XP)
- Or mark as missed (auto-reschedules)
- Complete revisions (+30 XP)

### 4. Analytics
- Weekly productivity charts
- Topic completion pie chart
- Subject-wise progress bars
- 30-day study streak calendar

### 5. Gamification
- Earn XP for activities
- Unlock badges
- Build study streaks
- View leaderboard

### 6. Question Bank
- Generate AI questions
- Choose MCQ, Short, or Long
- Select difficulty level
- Save to question bank

---

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "No such table"
**Solution:** Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Port already in use"
**Solution:** Use a different port
```bash
python manage.py runserver 8001
```

### Issue: "Static files not loading"
**Solution:** Create static directory
```bash
mkdir static
```

### Issue: "Permission denied" (Linux/Mac)
**Solution:** Make setup script executable
```bash
chmod +x setup.sh
```

---

## 📱 Navigation Guide

### Main Menu (Sidebar)
- **Dashboard** - Overview and stats
- **Upload Syllabus** - Add your syllabus
- **Subjects** - Manage subjects
- **Topics** - View all topics
- **Generate Schedule** - Create study plan
- **Calendar** - View schedule
- **Today's Tasks** - Daily tasks
- **Revisions** - Spaced repetition
- **Pomodoro Timer** - Study timer
- **Question Bank** - Practice questions
- **Analytics** - Progress insights
- **Badges** - Achievements

---

## 💡 Pro Tips

1. **Set Realistic Goals**: Don't overcommit on daily study hours
2. **Use Pomodoro**: Take breaks to maintain focus
3. **Complete Revisions**: Spaced repetition is key to retention
4. **Track Progress**: Check analytics weekly
5. **Build Streaks**: Study daily to maintain momentum
6. **Generate Questions**: Test yourself regularly
7. **Adjust Schedule**: Reschedule missed tasks promptly

---

## 🎯 Sample Workflow

### Daily Routine
1. **Morning**: Check "Today's Tasks"
2. **Study Session**: Use Pomodoro timer
3. **After Study**: Mark tasks complete
4. **Evening**: Review analytics
5. **Before Bed**: Check tomorrow's tasks

### Weekly Routine
1. **Monday**: Review weekly schedule
2. **Mid-week**: Complete pending revisions
3. **Friday**: Generate practice questions
4. **Weekend**: Catch up on missed tasks
5. **Sunday**: Plan next week

---

## 📊 Understanding XP System

### Earning XP
- Complete Task: **+50 XP**
- Complete Revision: **+30 XP**
- Complete Pomodoro: **+10 XP**

### Badges
- **7-Day Streak**: Study 7 days in a row
- **30-Day Streak**: Study 30 days in a row
- **100 Pomodoros**: Complete 100 sessions
- **All Topics Done**: Complete all topics
- **All Revisions Done**: Complete all revisions

---

## 🆘 Need Help?

### Documentation
- **README.md** - Full documentation
- **PROJECT_SUMMARY.md** - Project overview
- **TEMPLATES_GUIDE.md** - Template creation

### Support
- **GitHub Issues**: Report bugs
- **GitHub Discussions**: Ask questions
- **Email**: Contact repository owner

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Server starts without errors
- [ ] Can access landing page
- [ ] Can register new account
- [ ] Can login successfully
- [ ] Dashboard loads with stats
- [ ] Can upload/paste syllabus
- [ ] Topics are created
- [ ] Can generate schedule
- [ ] Pomodoro timer works
- [ ] Can mark tasks complete
- [ ] Analytics page shows charts
- [ ] Badges page displays
- [ ] Dark mode toggle works

---

## 🎉 You're All Set!

Your AI Study Planner is ready to use. Start by:
1. ✅ Uploading your syllabus
2. ✅ Generating your schedule
3. ✅ Starting your first Pomodoro session

**Happy studying! 📚🚀**

---

## 📞 Quick Links

- **Repository**: https://github.com/rr0h/ai-study-planner-productivity-engine
- **Issues**: https://github.com/rr0h/ai-study-planner-productivity-engine/issues
- **Django Docs**: https://docs.djangoproject.com/
- **Tailwind Docs**: https://tailwindcss.com/docs
