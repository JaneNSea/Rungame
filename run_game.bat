@echo off
echo ���� Pixel Runner Game...
echo.

REM ���Python�Ƿ�װ
python --version >nul 2>&1
if errorlevel 1 (
    echo ����: δ�ҵ�Python�����Ȱ�װPython 3.8����߰汾��
    pause
    exit /b 1
)

REM ��������Ƿ�װ
echo �����Ϸ����...
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo ��װ��Ϸ����...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ����: ������װʧ�ܡ�
        pause
        exit /b 1
    )
)

REM ������Ϸ
echo ������Ϸ...
python run_game.py

REM ��Ϸ��������ͣ
echo.
echo ��Ϸ�ѽ�����
pause
