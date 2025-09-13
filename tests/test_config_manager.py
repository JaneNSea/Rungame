import unittest
import tempfile
import os
import sys

# ���srcĿ¼��·��
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
        """����Ĭ�����ü���"""
        self.assertIsInstance(self.config_manager.config, dict)
        self.assertIn('game', self.config_manager.config)
        self.assertIn('physics', self.config_manager.config)
    
    def test_get_config_value(self):
        """���Ի�ȡ����ֵ"""
        fps = self.config_manager.get('game.fps')
        self.assertEqual(fps, 60)
        
        # ���Բ����ڵļ�
        non_existent = self.config_manager.get('non.existent.key', 'default')
        self.assertEqual(non_existent, 'default')
    
    def test_set_config_value(self):
        """������������ֵ"""
        self.config_manager.set('game.fps', 120)
        fps = self.config_manager.get('game.fps')
        self.assertEqual(fps, 120)
    
    def test_config_persistence(self):
        """�������ó־û�"""
        self.config_manager.set('test.value', 42)
        
        # �����µ����ù�����ʵ��
        new_config_manager = ConfigManager(self.config_file)
        test_value = new_config_manager.get('test.value')
        self.assertEqual(test_value, 42)

if __name__ == '__main__':
    unittest.main()
