import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file: str = "config/game_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"Failed to load config: {e}")
            return self.get_default_config()
    
    def save_config(self):
        """Save configuration file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "game": {
                "width": 480,
                "height": 270,
                "scale": 2,
                "fps": 60,
                "title": "Pixel Runner Game"
            },
            "physics": {
                "gravity": 0.5,
                "jump_strength": -10,
                "initial_obstacle_speed": 4,
                "speed_increase_rate": 0.2,
                "speed_increase_interval": 600
            }
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
