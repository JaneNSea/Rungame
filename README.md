# Pixel Runner Game

一个有趣的像素风格无限跑酷游戏，使用Python和Pygame开发。

## 特性

-  流畅的像素风格图形
-  收集星星获得额外分数
-  动态难度调整
-  炫酷的粒子效果
-  音效和背景音乐支持
-  高分记录系统
-  可配置的游戏设置

## 安装

### 使用pip安装

`ash
pip install -r requirements.txt
`

### 从源码安装

`ash
git clone <repository-url>
cd pixel-runner-game
pip install -e .
`

## 运行游戏

`ash
python enhanced_game.py
`

或者安装后：

`ash
pixel-runner
`

## 游戏控制

- **空格键**: 跳跃
- **P键**: 暂停/继续
- **R键**: 重新开始
- **ESC键**: 返回主菜单

## 游戏机制

### 分数系统
- 避过障碍物: +10分
- 收集星星: +50分
- 游戏速度会随时间增加

### 障碍物类型
-  尖刺: 细长的危险障碍
-  方块: 普通的方形障碍
-  锯齿: 旋转的圆形障碍
-  水晶: 闪亮的多边形障碍

## 配置

游戏配置文件位于 config/game_config.json，可以调整：
- 游戏窗口大小和FPS
- 物理参数（重力、跳跃力度等）
- 颜色主题
- 音频设置
- 控制键位

## 开发

### 项目结构

`
pixel-runner-game/
 enhanced_game.py      # 主游戏文件
 requirements.txt      # 依赖列表
 setup.py             # 安装配置
 config/              # 配置文件
    game_config.json
 assets/              # 游戏资源
 tests/               # 测试文件
 docs/                # 文档
`

### 运行测试

`ash
python -m pytest tests/
`

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
