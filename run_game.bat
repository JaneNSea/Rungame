@echo off
echo 启动 Pixel Runner Game...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python。请先安装Python 3.8或更高版本。
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查游戏依赖...
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo 安装游戏依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败。
        pause
        exit /b 1
    )
)

REM 运行游戏
echo 启动游戏...
python run_game.py

REM 游戏结束后暂停
echo.
echo 游戏已结束。
pause
