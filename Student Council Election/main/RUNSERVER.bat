@echo off
cd /d %~dp0
python.exe manage.py runserver
pause