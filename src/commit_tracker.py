"""
Commit Tracker Module
Tracks analyzed commits to avoid duplicates
"""
import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CommitTracker:
    def __init__(self, tracking_file: str = './data/analyzed_commits.json'):
        self.tracking_file = tracking_file
        self.data = self._load_tracking_data()
    
    def _load_tracking_data(self) -> dict:
        """Load tracking data from file"""
        try:
            if os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading tracking data: {str(e)}")
        
        return {'commits': {}}
    
    def _save_tracking_data(self) -> bool:
        """Save tracking data to file"""
        try:
            Path(self.tracking_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.tracking_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving tracking data: {str(e)}")
            return False
    
    def is_commit_analyzed(self, commit_hash: str) -> bool:
        """Check if a commit has already been analyzed"""
        return commit_hash in self.data['commits']
    
    def mark_commit_analyzed(self, commit_hash: str, analysis_results: dict, commit_info: dict = None) -> bool:
        """Mark a commit as analyzed"""
        try:
            self.data['commits'][commit_hash] = {
                'analysis_results': analysis_results,
                'commit_info': commit_info or {}
            }
            return self._save_tracking_data()
        except Exception as e:
            logger.error(f"Error marking commit as analyzed: {str(e)}")
            return False
    
    def get_all_analyzed_commits(self) -> list:
        """Get list of all analyzed commits"""
        return list(self.data['commits'].keys())
    
    def reset(self) -> bool:
        """Reset all tracking data"""
        try:
            self.data = {'commits': {}}
            logger.info("Tracking data reset")
            return self._save_tracking_data()
        except Exception as e:
            logger.error(f"Error resetting tracking data: {str(e)}")
            return False
