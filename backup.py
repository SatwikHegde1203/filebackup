import os
import shutil
import time

class BackupManager:
    def __init__(self):
        self.paused = False
        self.cancelled = False

    def backup_files(self, source_dir, backup_dir, progress_callback):
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        items = os.listdir(source_dir)
        total_items = len(items)
        completed_items = 0

        for item in items:
            if self.cancelled:
                progress_callback("Cancelled", 100)
                return "Backup cancelled."
            
            while self.paused:
                time.sleep(0.1)  # Wait while paused
            
            source_path = os.path.join(source_dir, item)
            backup_path = os.path.join(backup_dir, item)

            if os.path.isfile(source_path):
                shutil.copy2(source_path, backup_path)
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, backup_path, dirs_exist_ok=True)

            completed_items += 1
            progress_percentage = int((completed_items / total_items) * 100)
            progress_callback("Backing up", progress_percentage)

        return f"Backup completed from {source_dir} to {backup_dir}"

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def cancel(self):
        self.cancelled = True
