from typing import Dict, List, Any

class Achievement:
    def __init__(self, id: str, name: str, description: str, icon: str, condition_func):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.condition_func = condition_func
        self.unlocked = False

class AchievementManager:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.achievements = self._create_achievements()
        self.recently_unlocked = []
        
    def _create_achievements(self) -> Dict[str, Achievement]:
        achievements = {}
        
        achievements['first_100'] = Achievement(
            'first_100', 'First Steps', 'Reach 100 points', '',
            lambda stats: stats.get('score', 0) >= 100
        )
        
        achievements['score_500'] = Achievement(
            'score_500', 'Runner', 'Reach 500 points', '',
            lambda stats: stats.get('score', 0) >= 500
        )
        
        achievements['score_1000'] = Achievement(
            'score_1000', 'Expert Runner', 'Reach 1000 points', '',
            lambda stats: stats.get('score', 0) >= 1000
        )
        
        achievements['star_collector'] = Achievement(
            'star_collector', 'Star Collector', 'Collect 10 stars in one game', '',
            lambda stats: stats.get('stars_collected_in_game', 0) >= 10
        )
        
        achievements['speed_demon'] = Achievement(
            'speed_demon', 'Speed Demon', 'Reach speed 10', '',
            lambda stats: stats.get('max_speed', 0) >= 10
        )
        
        return achievements
    
    def check_achievements(self, game_stats: Dict[str, Any]) -> List[Achievement]:
        newly_unlocked = []
        
        for achievement in self.achievements.values():
            if not self.save_manager.is_achievement_unlocked(achievement.id):
                if achievement.condition_func(game_stats):
                    if self.save_manager.unlock_achievement(achievement.id, {
                        'name': achievement.name,
                        'description': achievement.description,
                        'icon': achievement.icon
                    }):
                        achievement.unlocked = True
                        newly_unlocked.append(achievement)
                        self.recently_unlocked.append(achievement)
        
        return newly_unlocked
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        unlocked = []
        save_data = self.save_manager.load_game_data()
        
        for achievement in self.achievements.values():
            if achievement.id in save_data.get('achievements', {}):
                achievement.unlocked = True
                unlocked.append(achievement)
        
        return unlocked
    
    def get_progress_info(self) -> Dict[str, Any]:
        total_achievements = len(self.achievements)
        unlocked_count = len(self.get_unlocked_achievements())
        
        return {
            'total': total_achievements,
            'unlocked': unlocked_count,
            'progress': unlocked_count / total_achievements if total_achievements > 0 else 0,
            'recently_unlocked': self.recently_unlocked
        }
    
    def clear_recent_achievements(self):
        self.recently_unlocked.clear()
