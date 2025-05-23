@echo off
cd /d %~dp0
python.exe manage.py import_users import-users.xlsx
pause