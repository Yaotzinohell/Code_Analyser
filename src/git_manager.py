"""
Git Manager Module
Handles cloning, pulling, and fetching commit information
"""
import os
import shutil
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class GitManager:
    def __init__(self, repo_url: str, repo_path: str = './repo_clone', branch: str = 'dev'):
        self.repo_url = repo_url
        self.repo_path = repo_path
        self.branch = branch
        self.repo = None
    
    def clone_or_update_repo(self) -> bool:
        """Clone the repository if it doesn't exist, otherwise update it."""
        try:
            try:
                from git import Repo, GitCommandError
            except ImportError:
                logger.error("GitPython not installed. Install with: pip install GitPython")
                return False
            
            if os.path.exists(self.repo_path):
                logger.info(f"Repository exists at {self.repo_path}. Updating...")
                self.repo = Repo(self.repo_path)
                self.repo.remotes.origin.pull(self.branch)
                logger.info("Repository updated successfully")
            else:
                logger.info(f"Cloning repository from {self.repo_url}")
                self.repo = Repo.clone_from(self.repo_url, self.repo_path, branch=self.branch)
                logger.info("Repository cloned successfully")
            
            return True
        except Exception as e:
            logger.error(f"Error cloning/updating repository: {str(e)}")
            return False
    
    def get_new_commits(self, since_commit: str = None) -> list:
        """Get all new commits since a specific commit."""
        try:
            from git import Repo
            
            if self.repo is None:
                self.repo = Repo(self.repo_path)
            
            if since_commit:
                commits = list(self.repo.iter_commits(f'{since_commit}..{self.branch}'))
            else:
                commits = list(self.repo.iter_commits(self.branch, max_count=100))
            
            logger.info(f"Found {len(commits)} commits")
            return commits
        except Exception as e:
            logger.error(f"Error getting commits: {str(e)}")
            return []
    
    def get_commit_details(self, commit) -> dict:
        """Extract commit details"""
        try:
            return {
                'hash': commit.hexsha,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'message': commit.message,
                'timestamp': datetime.fromtimestamp(commit.committed_date),
                'modified_files': list(commit.stats.files.keys())
            }
        except Exception as e:
            logger.error(f"Error getting commit details: {str(e)}")
            return {}
    
    def get_modified_files_in_commit(self, commit) -> list:
        """Get list of modified files in a commit"""
        try:
            return list(commit.stats.files.keys())
        except Exception as e:
            logger.error(f"Error getting modified files: {str(e)}")
            return []
    
    def cleanup(self) -> bool:
        """Remove the cloned repository"""
        try:
            if os.path.exists(self.repo_path):
                shutil.rmtree(self.repo_path)
                logger.info(f"Repository cleaned up")
                return True
        except Exception as e:
            logger.error(f"Error cleaning up repository: {str(e)}")
            return False
