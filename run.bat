@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -3 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist ".env" copy /Y ".env.example" ".env"
echo.
echo ==================================================
echo EduGenie server
 echo.
echo 1. Open .env and put your Gemini API key.
echo 2. Then run this file again.
echo 3. Open http://127.0.0.1:8000
 echo ==================================================
echo.
python -c "from pathlib import Path; t=Path('.env').read_text(); print('API key configured.' if 'paste_your_api_key_here' not in t else 'API key NOT configured yet.')"
uvicorn main:app --host 127.0.0.1 --port 8000
pause
