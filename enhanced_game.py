import pygame
import random
import sys
import math
import os
import json
from datetime import datetime

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 添加src目录到路径以导入自定义模块
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)
    try:
        from src.config_manager import ConfigManager
        from src.save_manager import SaveManager
        from src.achievements import AchievementManager
        ENHANCED_FEATURES = True
    except ImportError:
        ENHANCED_FEATURES = False
        print("警告: 无法加载高级功能模块，使用基础版本")
else:
    ENHANCED_FEATURES = False

# 屏幕大小（像素风比例）
WIDTH, HEIGHT = 480, 270
SCALE = 2  # 放大倍数
WIN = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Pixel Runner Game")

# 英文字体
PIXEL_FONT = pygame.font.Font(None, 24)
BIG_PIXEL_FONT = pygame.font.Font(None, 48)

# 颜色主题
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (46, 125, 50)
GROUND_SHADOW = (27, 94, 32)
PLAYER_COLOR = (33, 150, 243)
PLAYER_SHADOW = (21, 101, 192)
OBSTACLE_COLOR = (244, 67, 54)
OBSTACLE_SHADOW = (183, 28, 28)
SKY_COLOR = (135, 206, 235)
CLOUD_COLOR = (255, 255, 255, 180)
UI_COLOR = (76, 175, 80)
DEATH_OVERLAY = (0, 0, 0, 128)
BUTTON_COLOR = (76, 175, 80)
BUTTON_HOVER = (104, 159, 56)

# 游戏参数
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_SPEED = 4
SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1

# 游戏状态
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-5, -1)
        self.color = color
        self.life = 30
        self.max_life = 30
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2
        self.life -= 1
        
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color[:3], alpha)
            pygame.draw.circle(surface, self.color[:3], (int(self.x), int(self.y)), 2)

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 100)
        self.y = random.randint(20, 80)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(15, 25)
        
    def update(self):
        self.x -= self.speed
        
    def draw(self, surface):
        pygame.draw.circle(surface, CLOUD_COLOR[:3], (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(surface, CLOUD_COLOR[:3], (int(self.x + 10), int(self.y + 5)), self.size - 5)
        pygame.draw.circle(surface, CLOUD_COLOR[:3], (int(self.x - 10), int(self.y + 3)), self.size - 3)
        
    def off_screen(self):
        return self.x + self.size < 0

class Player:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.x = 50
        self.ground_y = HEIGHT - self.height - 20
        self.y = self.ground_y
        self.vel_y = 0
        self.on_ground = True
        self.animation_frame = 0
        self.jump_particles = []
        self.trail_particles = []

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            # 添加跳跃粒子效果
            for i in range(8):
                self.jump_particles.append(
                    Particle(self.x + self.width//2, self.y + self.height, PLAYER_COLOR)
                )

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # 碰到地面
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True

        # 更新动画
        self.animation_frame += 0.2
        
        # 添加尾迹粒子（跑步时）
        if self.on_ground and random.random() < 0.3:
            self.trail_particles.append(
                Particle(self.x + random.randint(0, self.width), 
                        self.y + self.height, 
                        (PLAYER_COLOR[0], PLAYER_COLOR[1], PLAYER_COLOR[2], 100))
            )
        
        # 更新粒子
        self.jump_particles = [p for p in self.jump_particles if p.life > 0]
        for particle in self.jump_particles:
            particle.update()
            
        self.trail_particles = [p for p in self.trail_particles if p.life > 0]
        for particle in self.trail_particles:
            particle.update()

    def draw(self, surface):
            
        # 绘制跳跃粒子
        for particle in self.jump_particles:
            particle.draw(surface)
            
        # 绘制阴影
        pygame.draw.rect(surface, PLAYER_SHADOW, 
                        (self.x + 1, self.y + 1, self.width, self.height))
        
        # 绘制主体（带简单动画）
        bob = int(math.sin(self.animation_frame) * 1) if self.on_ground else 0
        
        # 主体
        pygame.draw.rect(surface, PLAYER_COLOR, 
                        (self.x, self.y + bob, self.width, self.height))
        
        # 脸部区域（浅色）
        pygame.draw.rect(surface, (100, 180, 255), 
                        (self.x + 2, self.y + 2 + bob, self.width - 4, 8))
        
        # 绘制眼睛
        eye_color = WHITE
        pygame.draw.circle(surface, eye_color, (self.x + 4, self.y + 5 + bob), 2)
        pygame.draw.circle(surface, eye_color, (self.x + 12, self.y + 5 + bob), 2)
        pygame.draw.circle(surface, BLACK, (self.x + 5, self.y + 5 + bob), 1)
        pygame.draw.circle(surface, BLACK, (self.x + 13, self.y + 5 + bob), 1)
        
        # 绘制嘴巴（小微笑）
        mouth_y = self.y + 8 + bob
        pygame.draw.arc(surface, BLACK, (self.x + 6, mouth_y, 4, 3), 0, math.pi, 1)
        
        # 绘制手脚（简单的线条）
        if self.on_ground:
            # 脚
            pygame.draw.circle(surface, PLAYER_SHADOW, (self.x + 3, self.y + self.height + bob), 2)
            pygame.draw.circle(surface, PLAYER_SHADOW, (self.x + 13, self.y + self.height + bob), 2)

class Star:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.x = WIDTH + random.randint(0, 100)
        self.y = random.randint(HEIGHT//2, HEIGHT - 60)
        self.animation_frame = 0
        self.collected = False

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.animation_frame += 0.3

    def draw(self, surface):
        if not self.collected:
            # 绘制旋转的星星
            angle = self.animation_frame
            star_color = (255, 255, 0)  # 黄色
            glow_color = (255, 255, 200)  # 浅黄色
            
            # 绘制发光效果
            pygame.draw.circle(surface, glow_color, (int(self.x + 4), int(self.y + 4)), 6)
            
            # 绘制星星形状
            center_x, center_y = self.x + 4, self.y + 4
            size = 4
            points = []
            for i in range(10):
                radius = size if i % 2 == 0 else size // 2
                angle_point = angle + (i * math.pi / 5)
                x = center_x + radius * math.cos(angle_point)
                y = center_y + radius * math.sin(angle_point)
                points.append((x, y))
            
            pygame.draw.polygon(surface, star_color, points)

    def off_screen(self):
        return self.x + self.width < 0

    def check_collision(self, player):
        if not self.collected:
            if (player.x < self.x + self.width and
                player.x + player.width > self.x and
                player.y < self.y + self.height and
                player.y + player.height > self.y):
                self.collected = True
                return True
        return False

class Obstacle:
    def __init__(self):
        # 更多样化的障碍物类型
        obstacle_types = [
            {'width': 12, 'height': 24, 'type': 'spike'},     # 细长尖刺
            {'width': 20, 'height': 16, 'type': 'block'},     # 普通方块
            {'width': 16, 'height': 32, 'type': 'spike'},     # 高尖刺
            {'width': 24, 'height': 12, 'type': 'block'},     # 宽方块
            {'width': 18, 'height': 18, 'type': 'saw'},       # 锯齿状
            {'width': 14, 'height': 28, 'type': 'crystal'}    # 水晶障碍
        ]
        chosen = random.choice(obstacle_types)
        self.width = chosen['width']
        self.height = chosen['height']
        self.type = chosen['type']
        self.x = WIDTH
        self.y = HEIGHT - self.height - 20
        self.animation_frame = 0
        self.color = OBSTACLE_COLOR
        
        # 为不同类型设置不同颜色
        if self.type == 'saw':
            self.color = (255, 80, 80)  # 更红
        elif self.type == 'crystal':
            self.color = (100, 200, 255)  # 蓝色水晶

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.animation_frame += 0.1

    def draw(self, surface):
        # 根据障碍物类型绘制不同形状
        if self.type == 'spike':
            self.draw_spike(surface)
        elif self.type == 'block':
            self.draw_block(surface)
        elif self.type == 'saw':
            self.draw_saw(surface)
        elif self.type == 'crystal':
            self.draw_crystal(surface)

    def draw_spike(self, surface):
        # 绘制阴影
        pygame.draw.rect(surface, OBSTACLE_SHADOW, 
                        (self.x + 1, self.y + self.height//2 + 1, self.width, self.height//2))
        
        # 尖刺底座
        pygame.draw.rect(surface, self.color, 
                       (self.x, self.y + self.height//2, self.width, self.height//2))
        
        # 尖刺顶部（三角形）
        points = [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height//2),
            (self.x + self.width, self.y + self.height//2)
        ]
        pygame.draw.polygon(surface, self.color, points)
        
        # 高光效果
        highlight_points = [
            (self.x + self.width//2, self.y + 3),
            (self.x + 3, self.y + self.height//2 - 2),
            (self.x + self.width - 3, self.y + self.height//2 - 2)
        ]
        pygame.draw.polygon(surface, (255, 100, 100), highlight_points)

    def draw_block(self, surface):
        # 阴影
        pygame.draw.rect(surface, OBSTACLE_SHADOW, 
                       (self.x + 2, self.y + 2, self.width, self.height))
        
        # 主体
        pygame.draw.rect(surface, self.color, 
                       (self.x, self.y, self.width, self.height))
        
        # 添加纹理和细节
        for i in range(3, self.height, 4):
            pygame.draw.line(surface, OBSTACLE_SHADOW, 
                           (self.x, self.y + i), (self.x + self.width, self.y + i))
        
        # 添加边缘高光
        pygame.draw.line(surface, (255, 150, 150), 
                       (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(surface, (255, 150, 150), 
                       (self.x, self.y), (self.x, self.y + self.height), 2)

    def draw_saw(self, surface):
        # 锯齿状障碍物
        center_x, center_y = self.x + self.width // 2, self.y + self.height // 2
        radius = min(self.width, self.height) // 2
        small_radius = radius - 4
        
        # 阴影
        pygame.draw.circle(surface, OBSTACLE_SHADOW, (center_x + 2, center_y + 2), radius)
        
        # 主体
        pygame.draw.circle(surface, self.color, (center_x, center_y), radius)
        
        # 锯齿
        teeth = 8
        for i in range(teeth):
            angle = self.animation_frame + i * (2 * math.pi / teeth)
            x1 = center_x + math.cos(angle) * radius
            y1 = center_y + math.sin(angle) * radius
            x2 = center_x + math.cos(angle) * small_radius
            y2 = center_y + math.sin(angle) * small_radius
            pygame.draw.line(surface, (255, 255, 255), (x1, y1), (x2, y2), 2)
        
        # 中心圆
        pygame.draw.circle(surface, (255, 200, 200), (center_x, center_y), 4)

    def draw_crystal(self, surface):
        # 水晶障碍物
        center_x, center_y = self.x + self.width // 2, self.y + self.height // 2
        
        # 绘制水晶形状（六边形）
        points = []
        for i in range(6):
            angle = math.pi/3 * i + self.animation_frame
            radius = self.width//2 if i % 2 == 0 else self.height//2
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            points.append((x, y))
        
        # 阴影
        shadow_points = [(x+2, y+2) for x, y in points]
        pygame.draw.polygon(surface, OBSTACLE_SHADOW, shadow_points)
        
        # 主体
        pygame.draw.polygon(surface, self.color, points)
        
        # 高光效果
        pygame.draw.line(surface, (200, 230, 255), points[0], points[3], 1)
        pygame.draw.line(surface, (200, 230, 255), points[1], points[4], 1)
        pygame.draw.line(surface, (200, 230, 255), points[2], points[5], 1)

    def off_screen(self):
        return self.x + self.width < 0

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 将鼠标位置转换为游戏坐标
            scaled_pos = (event.pos[0] // SCALE, event.pos[1] // SCALE)
            if self.rect.collidepoint(scaled_pos):
                return True
        elif event.type == pygame.MOUSEMOTION:
            # 将鼠标位置转换为游戏坐标
            scaled_pos = (event.pos[0] // SCALE, event.pos[1] // SCALE)
            self.hovered = self.rect.collidepoint(scaled_pos)
        return False
    
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class Game:
    def __init__(self):
        global ENHANCED_FEATURES
        self.state = MENU
        self.player = Player()
        self.obstacles = []
        self.stars = []
        self.clouds = []
        self.particles = []
        self.score = 0
        self.stars_collected = 0
        self.high_score = 0
        self.obstacle_timer = 0
        self.star_timer = 0
        self.cloud_timer = 0
        self.difficulty_timer = 0
        self.screen_shake = 0

        # 初始化管理器（如果可用）
        self.config_manager = None
        self.save_manager = None
        self.achievement_manager = None

        if ENHANCED_FEATURES:
            try:
                self.config_manager = ConfigManager()
                self.save_manager = SaveManager()
                self.achievement_manager = AchievementManager(self.save_manager)
                # 从存档加载高分
                save_data = self.save_manager.load_game_data()
                self.high_score = save_data.get('high_score', 0)
                print("✓ 高级功能已启用：配置管理、存档系统、成就系统")
            except Exception as e:
                print(f"警告: 高级功能初始化失败: {e}")
                ENHANCED_FEATURES = False

        # 游戏统计
        self.game_stats = {
            'score': 0,
            'stars_collected_in_game': 0,
            'obstacles_avoided': 0,
            'obstacles_avoided_streak': 0,
            'star_streak': 0,
            'max_speed': 0,
            'perfect_start': True,
            'game_start_time': None
        }

        # 字体
        self.font = PIXEL_FONT
        self.big_font = BIG_PIXEL_FONT

        # 按钮 - 使用英文避免字体问题
        self.play_button = Button(WIDTH//2 - 50, HEIGHT//2, 100, 30, "PLAY", self.font)
        self.restart_button = Button(WIDTH//2 - 50, HEIGHT//2 + 20, 100, 30, "RESTART", self.font)
        self.menu_button = Button(WIDTH//2 - 50, HEIGHT//2 + 60, 100, 30, "MENU", self.font)

        # 成就通知
        self.achievement_notifications = []
        self.notification_timer = 0
        
    def reset_game(self):
        global OBSTACLE_SPEED
        OBSTACLE_SPEED = 4
        self.player = Player()
        self.obstacles = []
        self.stars = []
        self.particles = []
        self.score = 0
        self.stars_collected = 0
        self.obstacle_timer = 0
        self.star_timer = 0
        self.difficulty_timer = 0
        self.screen_shake = 0
        pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, 1500)
        
        # 重置游戏统计
        self.game_stats = {
            'score': 0,
            'stars_collected_in_game': 0,
            'obstacles_avoided': 0,
            'obstacles_avoided_streak': 0,
            'star_streak': 0,
            'max_speed': OBSTACLE_SPEED,
            'perfect_start': True,
            'game_start_time': datetime.now()
        }
        
        # 增加游戏次数
        if self.save_manager:
            self.save_manager.increment_games_played()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if self.state == MENU:
                if self.play_button.handle_event(event):
                    self.state = PLAYING
                    self.reset_game()
                    
            elif self.state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                if event.type == SPAWN_OBSTACLE_EVENT:
                    self.obstacles.append(Obstacle())
                    
            elif self.state == GAME_OVER:
                if self.restart_button.handle_event(event):
                    self.state = PLAYING
                    self.reset_game()
                elif self.menu_button.handle_event(event):
                    self.state = MENU
                    
        return True
    
    def update(self):
        if self.state == PLAYING:
            # 更新玩家
            self.player.update()
            
            # 更新障碍物
            for obs in self.obstacles:
                obs.update()
            
            # 更新星星
            for star in self.stars:
                star.update()
                
            # 检查星星收集
            stars_collected_this_frame = 0
            for star in self.stars:
                if star.check_collision(self.player):
                    self.stars_collected += 1
                    stars_collected_this_frame += 1
                    self.score += 50
                    
                    # 更新统计
                    self.game_stats['stars_collected_in_game'] += 1
                    self.game_stats['star_streak'] += 1
                    
                    # 添加收集粒子效果
                    for i in range(15):
                        self.particles.append(
                            Particle(star.x + 4, star.y + 4, (255, 255, 0))
                        )
            
            # 如果这一帧没有收集到星星，重置连击
            if stars_collected_this_frame == 0:
                if len([s for s in self.stars if s.x < self.player.x + self.player.width]) > 0:
                    self.game_stats['star_streak'] = 0
            
            # 移除屏幕外障碍物并增加分数
            old_count = len(self.obstacles)
            self.obstacles = [obs for obs in self.obstacles if not obs.off_screen()]
            obstacles_passed = old_count - len(self.obstacles)
            self.score += obstacles_passed * 10
            
            # 更新统计
            self.game_stats['obstacles_avoided'] += obstacles_passed
            self.game_stats['obstacles_avoided_streak'] += obstacles_passed
            
            # 移除屏幕外的星星
            self.stars = [star for star in self.stars if not star.off_screen()]
            
            # 生成星星
            self.star_timer += 1
            if self.star_timer > 180:  # 每3秒生成星星
                if random.random() < 0.7:  # 70%概率生成星星
                    self.stars.append(Star())
                self.star_timer = 0
            
            # 更新云朵
            self.cloud_timer += 1
            if self.cloud_timer > 120:  # 每2秒生成云朵
                self.clouds.append(Cloud())
                self.cloud_timer = 0
                
            for cloud in self.clouds:
                cloud.update()
            self.clouds = [cloud for cloud in self.clouds if not cloud.off_screen()]
            
            # 增加难度
            self.difficulty_timer += 1
            if self.difficulty_timer > 600:  # 每10秒增加难度
                global OBSTACLE_SPEED
                OBSTACLE_SPEED += 0.2
                spawn_rate = max(800, 1500 - self.difficulty_timer // 60 * 50)
                pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, spawn_rate)
                self.difficulty_timer = 0
            
            # 更新统计
            self.game_stats['score'] = self.score
            self.game_stats['max_speed'] = max(self.game_stats['max_speed'], OBSTACLE_SPEED)
            
            # 检查完美开局
            if self.score > 100 and self.game_stats['obstacles_avoided_streak'] > 0:
                pass  # 保持完美开局状态
            elif self.score > 100:
                self.game_stats['perfect_start'] = False
            
            # 碰撞检测
            for obs in self.obstacles:
                if (self.player.x < obs.x + obs.width and
                    self.player.x + self.player.width > obs.x and
                    self.player.y < obs.y + obs.height and
                    self.player.y + self.player.height > obs.y):
                    
                    # 重置连击计数
                    self.game_stats['obstacles_avoided_streak'] = 0
                    if self.score <= 100:
                        self.game_stats['perfect_start'] = False
                    
                    # 添加死亡粒子效果
                    for i in range(20):
                        self.particles.append(
                            Particle(self.player.x + self.player.width//2, 
                                   self.player.y + self.player.height//2, PLAYER_COLOR)
                        )
                    
                    # 屏幕震动效果
                    self.screen_shake = 10
                    
                    # 游戏结束处理
                    self.handle_game_over()
                    self.state = GAME_OVER
        
        # 更新屏幕震动
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # 更新粒子
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.life > 0]
        
        # 更新成就通知计时器
        if self.notification_timer > 0:
            self.notification_timer -= 1
        elif self.achievement_notifications:
            self.achievement_notifications.clear()
    
    def handle_game_over(self):
        """处理游戏结束时的逻辑"""
        # 更新高分
        if self.score > self.high_score:
            self.high_score = self.score
            
        # 保存数据和检查成就
        if ENHANCED_FEATURES and self.save_manager and self.achievement_manager:
            # 更新存档数据
            is_new_high_score = self.save_manager.update_high_score(self.score)
            self.save_manager.add_stars(self.game_stats['stars_collected_in_game'])
            
            # 更新统计数据
            save_data = self.save_manager.load_game_data()
            stats_to_save = {
                'longest_run': max(save_data.get('statistics', {}).get('longest_run', 0), self.score),
                'highest_speed': max(save_data.get('statistics', {}).get('highest_speed', 0), self.game_stats['max_speed']),
                'obstacles_avoided': save_data.get('statistics', {}).get('obstacles_avoided', 0) + self.game_stats['obstacles_avoided'],
                'stars_collected': save_data.get('statistics', {}).get('stars_collected', 0) + self.game_stats['stars_collected_in_game']
            }
            self.save_manager.update_statistics(stats_to_save)
            
            # 准备成就检查数据
            updated_save_data = self.save_manager.load_game_data()
            achievement_data = {
                **self.game_stats,
                'total_stars_collected': updated_save_data.get('total_stars_collected', 0),
                'total_games_played': updated_save_data.get('total_games_played', 0),
                'is_new_high_score': is_new_high_score
            }
            
            # 检查成就
            new_achievements = self.achievement_manager.check_achievements(achievement_data)
            if new_achievements:
                print(f"✨ 解锁了 {len(new_achievements)} 个新成就！")
                for achievement in new_achievements:
                    print(f"🏆 {achievement.name}: {achievement.description}")
                    self.achievement_notifications.append(achievement)
                self.notification_timer = 300  # 显示5秒
    
    def draw(self):
        # 创建主画布
        surface = pygame.Surface((WIDTH, HEIGHT))
        
        # 绘制天空渐变
        for y in range(HEIGHT - 20):
            color_ratio = y / (HEIGHT - 20)
            r = int(SKY_COLOR[0] * (1 - color_ratio) + WHITE[0] * color_ratio)
            g = int(SKY_COLOR[1] * (1 - color_ratio) + WHITE[1] * color_ratio)
            b = int(SKY_COLOR[2] * (1 - color_ratio) + WHITE[2] * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
        
        # 绘制云朵
        for cloud in self.clouds:
            cloud.draw(surface)
        
        # 绘制地面（带纹理）
        pygame.draw.rect(surface, GROUND_SHADOW, (0, HEIGHT - 18, WIDTH, 18))
        pygame.draw.rect(surface, GROUND_COLOR, (0, HEIGHT - 20, WIDTH, 18))
        # 地面纹理
        for x in range(0, WIDTH, 8):
            pygame.draw.line(surface, GROUND_SHADOW, (x, HEIGHT - 20), (x, HEIGHT - 2))
        
        if self.state == MENU:
            self.draw_menu(surface)
        elif self.state == PLAYING:
            self.draw_game(surface)
        elif self.state == GAME_OVER:
            self.draw_game_over(surface)
        
        # 应用屏幕震动效果
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # 放大显示
        scaled_surface = pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE))
        WIN.fill(BLACK)  # 清除屏幕
        WIN.blit(scaled_surface, (shake_x, shake_y))
        pygame.display.update()
    
    def draw_menu(self, surface):
        # 背景渐变效果
        for y in range(HEIGHT//3):
            alpha = 100 * (1 - y/(HEIGHT/3))
            pygame.draw.line(surface, (*BUTTON_COLOR, int(alpha)), (0, y), (WIDTH, y))
        
        # 标题 - 更大更醒目
        title = BIG_PIXEL_FONT.render("PIXEL RUNNER", True, BLACK)
        title_shadow = BIG_PIXEL_FONT.render("PIXEL RUNNER", True, PLAYER_SHADOW)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        surface.blit(title_shadow, (title_rect.x+2, title_rect.y+2))
        surface.blit(title, title_rect)
        
        # 版本信息 - 右上角
        if ENHANCED_FEATURES:
            version_text = self.font.render("v2.0 Runner", True, (0, 100, 0))
            surface.blit(version_text, (WIDTH - 100, 10))
        
        # 最高分 - 更突出
        if self.high_score > 0:
            score_bg = pygame.Rect(WIDTH//2 - 75, HEIGHT//3, 150, 25)
            pygame.draw.rect(surface, (*BUTTON_COLOR, 150), score_bg)
            pygame.draw.rect(surface, BLACK, score_bg, 1)
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
            high_score_rect = high_score_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 12))
            surface.blit(high_score_text, high_score_rect)
        
        # 信息面板 - 左侧
        info_start_y = HEIGHT//2 - 40
        info_x = 20
        
        # 显示统计信息（如果可用）
        if ENHANCED_FEATURES and self.save_manager:
            save_data = self.save_manager.load_game_data()
            total_stars = save_data.get('total_stars_collected', 0)
            total_games = save_data.get('total_games_played', 0)
            
            # 统计面板背景
            stats_panel = pygame.Rect(info_x - 5, info_start_y - 5, 150, 80)
            pygame.draw.rect(surface, (255, 255, 255, 120), stats_panel)
            pygame.draw.rect(surface, BLACK, stats_panel, 1)
            
            # 统计标题
            stats_title = self.font.render("Statistics:", True, BLACK)
            surface.blit(stats_title, (info_x, info_start_y))
            
            if total_stars > 0:
                stars_text = self.font.render(f"⭐ Stars: {total_stars}", True, (180, 150, 0))
                surface.blit(stars_text, (info_x, info_start_y + 20))
            
            if total_games > 0:
                games_text = self.font.render(f"🎮 Games: {total_games}", True, BLACK)
                surface.blit(games_text, (info_x, info_start_y + 40))
            
            # 成就进度
            if self.achievement_manager:
                progress = self.achievement_manager.get_progress_info()
                achievement_text = self.font.render(f"🏆 Achievements: {progress['unlocked']}", True, BLACK)
                surface.blit(achievement_text, (info_x, info_start_y + 60))
        
        # 按钮 - 居中放置，调整大小
        self.play_button.rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 30, 120, 40)
        self.play_button.draw(surface)
        
        # 操作提示 - 底部
        hint_bg = pygame.Rect(WIDTH//2 - 100, HEIGHT - 40, 200, 25)
        pygame.draw.rect(surface, (255, 255, 255, 150), hint_bg)
        pygame.draw.rect(surface, BLACK, hint_bg, 1)
        hint = self.font.render("Press SPACE to Jump", True, BLACK)
        hint_rect = hint.get_rect(center=(WIDTH//2, HEIGHT - 28))
        surface.blit(hint, hint_rect)
        
        # 装饰元素：添加一些简单的游戏角色
        pygame.draw.rect(surface, PLAYER_SHADOW, (WIDTH - 50, HEIGHT - 41, 16, 16))
        pygame.draw.rect(surface, PLAYER_COLOR, (WIDTH - 52, HEIGHT - 43, 16, 16))
        pygame.draw.rect(surface, OBSTACLE_SHADOW, (WIDTH - 80, HEIGHT - 41, 16, 16))
        pygame.draw.rect(surface, OBSTACLE_COLOR, (WIDTH - 82, HEIGHT - 43, 16, 16))
    
    def draw_game(self, surface):
        # 绘制星星
        for star in self.stars:
            star.draw(surface)
            
        # 绘制玩家和障碍
        self.player.draw(surface)
        for obs in self.obstacles:
            obs.draw(surface)
        
        # 绘制粒子
        for particle in self.particles:
            particle.draw(surface)
        
        # UI面板背景
        pygame.draw.rect(surface, (0, 0, 0, 150), (5, 5, 180, 55))
        pygame.draw.rect(surface, BUTTON_COLOR, (5, 5, 180, 55), 2)
        
        # 显示分数
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # 显示星星收集数
        stars_text = self.font.render(f"Stars: {self.stars_collected}", True, (255, 255, 0))
        surface.blit(stars_text, (10, 25))
        
        # 显示速度
        speed_text = self.font.render(f"Speed: {OBSTACLE_SPEED:.1f}", True, WHITE)
        surface.blit(speed_text, (10, 40))
        
        # 显示成就通知
        self.draw_achievement_notifications(surface)
    
    def draw_achievement_notifications(self, surface):
        """绘制成就通知"""
        if self.achievement_notifications and self.notification_timer > 0:
            # 计算通知位置
            notification_y = 70
            for i, achievement in enumerate(self.achievement_notifications[:3]):  # 最多显示3个
                # 背景
                notification_bg = pygame.Surface((280, 30))
                notification_bg.set_alpha(200)
                notification_bg.fill((50, 50, 50))
                surface.blit(notification_bg, (WIDTH - 290, notification_y + i * 35))
                
                # 边框
                pygame.draw.rect(surface, (255, 215, 0), (WIDTH - 290, notification_y + i * 35, 280, 30), 2)
                
                # 文本
                achievement_text = self.font.render(f"🏆 {achievement.name}", True, (255, 215, 0))
                surface.blit(achievement_text, (WIDTH - 285, notification_y + i * 35 + 5))
                
                desc_text = self.font.render(achievement.description, True, WHITE)
                surface.blit(desc_text, (WIDTH - 285, notification_y + i * 35 + 15))
    
    def draw_game_over(self, surface):
        # 绘制游戏画面（暗化）
        self.draw_game(surface)
        
        # 半透明覆盖
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # 游戏结束文本
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
        surface.blit(game_over_text, game_over_rect)
        
        # 最终分数
        final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        surface.blit(final_score, final_score_rect)
        
        # 星星收集数
        stars_final = self.font.render(f"Stars Collected: {self.stars_collected}", True, (255, 255, 0))
        stars_final_rect = stars_final.get_rect(center=(WIDTH//2, HEIGHT//2 - 35))
        surface.blit(stars_final, stars_final_rect)
        
        # 最高分
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
        surface.blit(high_score_text, high_score_rect)
        
        # 按钮
        self.restart_button.draw(surface)
        self.menu_button.draw(surface)

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        if not game.handle_events():
            break
        
        game.update()
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
