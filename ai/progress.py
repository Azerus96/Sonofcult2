# ai/progress.py
import os
import json
from datetime import datetime
from typing import Dict, Optional

class ProgressManager:
    def __init__(self, token: str, progress_dir: str = 'progress'):
        self.token = token
        self.progress_dir = progress_dir
        self.ensure_progress_dir()
        
    def ensure_progress_dir(self):
        """Создает директорию для прогресса, если она не существует"""
        if not os.path.exists(self.progress_dir):
            os.makedirs(self.progress_dir)
            
    def get_progress_path(self, timestamp: Optional[str] = None) -> str:
        """Формирует путь к файлу прогресса"""
        if timestamp:
            filename = f'progress_{self.token}_{timestamp}.json'
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'progress_{self.token}_{timestamp}.json'
        return os.path.join(self.progress_dir, filename)
        
    def save_progress(self, state: Dict):
        """Сохраняет текущий прогресс"""
        path = self.get_progress_path()
        
        progress_data = {
            'timestamp': datetime.now().isoformat(),
            'state': state
        }
        
        with open(path, 'w') as f:
            json.dump(progress_data, f, indent=2)
            
    def load_latest_progress(self) -> Optional[Dict]:
        """Загружает последний сохраненный прогресс"""
        files = [f for f in os.listdir(self.progress_dir) 
                if f.startswith(f'progress_{self.token}_')]
                
        if not files:
            return None
            
        latest_file = max(files)
        path = os.path.join(self.progress_dir, latest_file)
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return data['state']
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return None
            
    def clean_old_progress(self, keep_days: int = 7):
        """Удаляет старые файлы прогресса"""
        current_time = datetime.now()
        files = os.listdir(self.progress_dir)
        
        for file in files:
            if not file.startswith(f'progress_{self.token}_'):
                continue
                
            file_path = os.path.join(self.progress_dir, file)
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            
            if (current_time - file_time).days > keep_days:
                os.remove(file_path)
