# 开发者文档

## 项目结构

### 核心模块

#### src/config_manager.py
配置管理系统，负责：
- 加载和保存游戏配置
- 提供配置的getter/setter接口
- 管理默认配置

#### src/save_manager.py
存档管理系统，负责：
- 游戏数据的持久化存储
- 高分记录管理
- 游戏统计数据跟踪
- 成就数据管理

#### src/achievements.py
成就系统，提供：
- 成就定义和条件检查
- 成就解锁逻辑
- 成就进度跟踪

### 游戏架构

#### 状态管理
游戏使用状态机模式：
- MENU - 主菜单状态
- PLAYING - 游戏进行状态  
- GAME_OVER - 游戏结束状态
- PAUSED - 游戏暂停状态（可扩展）

#### 游戏对象
- Player - 玩家角色
- Obstacle - 障碍物（多种类型）
- Star - 可收集的星星
- Cloud - 背景云朵
- Particle - 粒子效果

#### 渲染系统
- 像素完美渲染（整数坐标）
- 分层渲染：背景 -> 游戏对象 -> 粒子 -> UI
- 屏幕震动效果
- 缩放支持

## 开发环境设置

### 依赖安装
`ash
pip install -r requirements.txt
`

### 运行测试
`ash
python -m pytest tests/ -v
`

### 代码风格
- 使用PEP 8代码风格
- 类型提示（Python 3.8+）
- 详细的文档字符串

## 扩展功能指南

### 添加新的障碍物类型

1. 在 Obstacle 类中添加新的绘制方法：
`python
def draw_new_obstacle_type(self, surface):
    # 实现新障碍物的绘制逻辑
    pass
`

2. 在障碍物类型列表中添加新类型：
`python
obstacle_types = [
    # 现有类型...
    {'width': 20, 'height': 20, 'type': 'new_type'}
]
`

### 添加新成就

1. 在 AchievementManager._create_achievements() 中添加：
`python
achievements['new_achievement'] = Achievement(
    'new_achievement', 
    '成就名称', 
    '成就描述', 
    '',
    lambda stats: stats.get('condition', 0) >= target_value
)
`

### 添加新的配置选项

1. 在 ConfigManager.get_default_config() 中添加默认值
2. 在 config/game_config.json 中添加配置
3. 在相关代码中使用 config.get('section.key') 获取

### 音效集成

项目已准备好音效系统框架：
1. 在 ssets/ 目录中添加音效文件
2. 在配置中启用音效
3. 使用 pygame.mixer 播放音效

## 性能优化

### 渲染优化
- 使用对象池减少内存分配
- 批量渲染相同类型的对象
- 视野裁剪（仅渲染屏幕内的对象）

### 内存管理
- 及时清理屏幕外的对象
- 限制粒子数量
- 重用游戏对象

## 调试技巧

### 调试模式
可以添加调试开关来显示：
- 碰撞盒
- FPS计数器
- 内存使用情况
- 对象计数

### 日志记录
使用Python的logging模块记录关键事件：
`python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
`

## 发布准备

### 构建可执行文件
使用PyInstaller打包：
`ash
pip install pyinstaller
pyinstaller --onefile --windowed run_game.py
`

### 资源打包
确保所有资源文件都包含在发布版本中：
- 配置文件
- 音效文件（如果有）
- 字体文件（如果有）

## 贡献指南

1. Fork项目
2. 创建feature分支
3. 提交更改
4. 运行测试确保通过
5. 提交Pull Request

### 提交信息格式
`
type(scope): description

body

footer
`

类型：
- feat: 新功能
- fix: 错误修复
- docs: 文档更改
- style: 代码风格更改
- refactor: 代码重构
- test: 测试相关
- chore: 其他更改
