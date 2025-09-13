import json
import os
from datetime import datetime
from typing import Dict, Any

class SaveManager:
    def __init__(self, save_dir: str = "game_data"):
        self.save_dir = save_dir
        self.save_file = os.path.join(save_dir, "save_data.json")
        self.ensure_save_dir()
        
    def ensure_save_dir(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def save_game_data(self, data: Dict[str, Any]):
        try:
            save_data = self.load_game_data()
            save_data.update(data)
            save_data['last_save'] = datetime.now().isoformat()
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Save failed: {e}")
    
    def load_game_data(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_save_data()
        except Exception as e:
            print(f"Load failed: {e}")
            return self.get_default_save_data()
    
    def get_default_save_data(self) -> Dict[str, Any]:
        return {
            'high_score': 0,
            'total_stars_collected': 0,
            'total_games_played': 0,
            'achievements': {},
            'statistics': {
                'longest_run': 0,
                'highest_speed': 0,
                'obstacles_avoided': 0,
                'stars_collected': 0
            }
        }
    
    def update_high_score(self, score: int) -> bool:
        data = self.load_game_data()
        if score > data.get('high_score', 0):
            data['high_score'] = score
            self.save_game_data(data)
            return True
        return False
    
    def add_stars(self, stars: int):
        data = self.load_game_data()
        data['total_stars_collected'] = data.get('total_stars_collected', 0) + stars
        self.save_game_data(data)
    
    def increment_games_played(self):
        data = self.load_game_data()
        data['total_games_played'] = data.get('total_games_played', 0) + 1
        self.save_game_data(data)
    
    def update_statistics(self, stats: Dict[str, Any]):
        data = self.load_game_data()
        if 'statistics' not in data:
            data['statistics'] = {}
        data['statistics'].update(stats)
        self.save_game_data(data)
    
    def unlock_achievement(self, achievement_id: str, achievement_data: Dict[str, Any]):
        data = self.load_game_data()
        if 'achievements' not in data:
            data['achievements'] = {}
        if achievement_id not in data['achievements']:
            data['achievements'][achievement_id] = {
                **achievement_data,
                'unlocked_at': datetime.now().isoformat()
            }
            self.save_game_data(data)
            return True
        return False
    
    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        data = self.load_game_data()
        return achievement_id in data.get('achievements', {})
