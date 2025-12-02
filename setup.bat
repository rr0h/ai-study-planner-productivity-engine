@echo off
echo 🎓 AI Study Planner Setup Script
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create static directory
echo 📁 Creating static directory...
if not exist "static" mkdir static

REM Create media directory
echo 📁 Creating media directory...
if not exist "media" mkdir media

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser prompt
echo.
set /p create_superuser="👤 Would you like to create a superuser? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the development server:
echo    1. Activate virtual environment: venv\Scripts\activate
echo    2. Run server: python manage.py runserver
echo    3. Open browser: http://127.0.0.1:8000/
echo.
echo 📚 Happy studying!
pause
