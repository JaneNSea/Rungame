import unittest
import tempfile
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        self.config_manager = ConfigManager(self.config_file)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_default_config_loading(self):
        """测试默认配置加载"""
        self.assertIsInstance(self.config_manager.config, dict)
        self.assertIn('game', self.config_manager.config)
        self.assertIn('physics', self.config_manager.config)
    
    def test_get_config_value(self):
        """测试获取配置值"""
        fps = self.config_manager.get('game.fps')
        self.assertEqual(fps, 60)
        
        # 测试不存在的键
        non_existent = self.config_manager.get('non.existent.key', 'default')
        self.assertEqual(non_existent, 'default')
    
    def test_set_config_value(self):
        """测试设置配置值"""
        self.config_manager.set('game.fps', 120)
        fps = self.config_manager.get('game.fps')
        self.assertEqual(fps, 120)
    
    def test_config_persistence(self):
        """测试配置持久化"""
        self.config_manager.set('test.value', 42)
        
        # 创建新的配置管理器实例
        new_config_manager = ConfigManager(self.config_file)
        test_value = new_config_manager.get('test.value')
        self.assertEqual(test_value, 42)

if __name__ == '__main__':
    unittest.main()
