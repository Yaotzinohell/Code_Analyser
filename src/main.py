"""
Main Orchestrator
Coordinates AI analysis, Git management, and email notifications
"""
import os
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Setup logging
def setup_logging(log_file: str = './logs/code_analyzer.log'):
    """Setup logging configuration"""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


setup_logging()
logger = logging.getLogger(__name__)


class AICodeAnalyzerOrchestrator:
    def __init__(self):
        try:
            from src.git_manager import GitManager
            from src.email_notifier import EmailNotifier
            from src.commit_tracker import CommitTracker
            from src.ai_analyzer import get_analyzer
            from config.config import (
                REPO_URL, REPO_BRANCH, REPO_LOCAL_PATH,
                AI_PROVIDER, EMAIL_SENDER, EMAIL_PASSWORD,
                EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, TRACKED_COMMITS_FILE
            )
            
            self.git_manager = GitManager(REPO_URL, REPO_LOCAL_PATH, REPO_BRANCH)
            self.ai_analyzer = get_analyzer(AI_PROVIDER)
            self.email_notifier = EmailNotifier(EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
            self.commit_tracker = CommitTracker(TRACKED_COMMITS_FILE)
            
            self.repo_url = REPO_URL
            self.repo_branch = REPO_BRANCH
            self.repo_path = REPO_LOCAL_PATH
            
            logger.info("AI Code Analyzer Orchestrator initialized")
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise
    
    def run(self) -> Dict:
        """Main execution flow"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'commits_analyzed': 0,
            'issues_found': 0,
            'emails_sent': 0,
            'status': 'success'
        }
        
        try:
            # Step 1: Clone/update repository
            logger.info("Step 1: Cloning/updating repository...")
            if not self.git_manager.clone_or_update_repo():
                logger.error("Failed to clone/update repository")
                summary['status'] = 'failed'
                return summary
            
            # Step 2: Get new commits
            logger.info("Step 2: Fetching new commits...")
            analyzed_commits = self.commit_tracker.get_all_analyzed_commits()
            last_commit = analyzed_commits[-1] if analyzed_commits else None
            new_commits = self.git_manager.get_new_commits(last_commit)
            
            if not new_commits:
                logger.info("No new commits to analyze")
                return summary
            
            logger.info(f"Found {len(new_commits)} new commits to analyze")
            
            # Step 3: Analyze each commit
            logger.info("Step 3: Analyzing commits...")
            for commit in reversed(new_commits):  # Oldest first
                commit_details = self.git_manager.get_commit_details(commit)
                commit_hash = commit_details.get('hash')
                
                logger.info(f"Analyzing commit {commit_hash[:8]}...")
                
                # Get modified files
                modified_files = self.git_manager.get_modified_files_in_commit(commit)
                
                # Analyze files
                error_reports = self._analyze_commit_files(modified_files)
                
                if error_reports:
                    summary['issues_found'] += len(error_reports)
                    
                    # Send notifications
                    logger.info(f"Sending notifications for {len(error_reports)} file(s) with issues...")
                    self._send_notifications(commit_details, error_reports)
                    summary['emails_sent'] += 1
                
                # Mark as analyzed
                self.commit_tracker.mark_commit_analyzed(
                    commit_hash,
                    {'files_analyzed': len(modified_files), 'issues': len(error_reports)},
                    commit_details
                )
                summary['commits_analyzed'] += 1
            
            logger.info(f"Analysis complete. Summary: {summary}")
            return summary
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            summary['status'] = 'failed'
            summary['error'] = str(e)
            return summary
    
    def _analyze_commit_files(self, modified_files: List[str]) -> List[Dict]:
        """Analyze files in a commit"""
        error_reports = []
        
        try:
            for file_path in modified_files:
                # Skip certain files
                if file_path.endswith('qn.txt') or file_path.startswith('.'):
                    continue
                
                # Get folder name
                path_parts = file_path.split('/')
                if len(path_parts) < 2:
                    continue
                
                folder_name = path_parts[0]
                file_name = path_parts[-1]
                
                # Check if code file
                from pathlib import Path
                ext = Path(file_path).suffix
                if ext not in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php', '.swift']:
                    continue
                
                # Get full path
                full_file_path = os.path.join(self.repo_path, file_path)
                
                # Analyze with AI
                analysis = self.ai_analyzer.analyze_file(full_file_path)
                
                # Check if errors found
                if analysis.get('has_errors') or analysis.get('errors'):
                    error_reports.append({
                        'folder_name': folder_name,
                        'file_name': file_name,
                        'file_path': file_path,
                        'analysis': analysis
                    })
                    
                    error_count = len(analysis.get('errors', []))
                    logger.info(f"Issues found in {folder_name}/{file_name}: {error_count} issue(s)")
        
        except Exception as e:
            logger.error(f"Error analyzing commit files: {str(e)}")
        
        return error_reports
    
    def _send_notifications(self, commit_details: Dict, error_reports: List[Dict]) -> None:
        """Send email notifications"""
        try:
            author_email = commit_details.get('author_email')
            author_name = commit_details.get('author_name')
            
            # Group by folder
            errors_by_folder = {}
            for report in error_reports:
                folder = report['folder_name']
                if folder not in errors_by_folder:
                    errors_by_folder[folder] = []
                errors_by_folder[folder].append(report)
            
            # Send emails
            for folder_name, folder_errors in errors_by_folder.items():
                analysis_results = {
                    'files': [err['analysis'] for err in folder_errors]
                }
                
                self.email_notifier.send_error_notification(
                    recipient_email=author_email,
                    author_name=author_name,
                    branch=self.repo_branch,
                    folder_name=folder_name,
                    analysis_results=analysis_results
                )
        
        except Exception as e:
            logger.error(f"Error sending notifications: {str(e)}")
    
    def test_setup(self) -> Dict:
        """Test if all components are configured"""
        results = {
            'ai_configured': False,
            'email_configured': False,
            'repo_accessible': False,
            'details': {}
        }
        
        try:
            # Test AI
            logger.info("Testing AI configuration...")
            try:
                # Try a simple test (don't actually call AI if not needed)
                if self.ai_analyzer:
                    results['ai_configured'] = True
                    results['details']['ai_provider'] = 'Configured'
            except Exception as e:
                results['details']['ai_error'] = str(e)
            
            # Test email
            logger.info("Testing email configuration...")
            if self.email_notifier.test_email_configuration():
                results['email_configured'] = True
                results['details']['email'] = 'Test email sent successfully'
            else:
                results['details']['email'] = 'Test email failed'
            
            # Test git
            logger.info("Testing repository access...")
            if self.git_manager.clone_or_update_repo():
                results['repo_accessible'] = True
                results['details']['repo'] = f'Repository accessible: {self.repo_url}'
            
            logger.info(f"Setup test results: {results}")
            return results
        
        except Exception as e:
            logger.error(f"Error during setup test: {str(e)}")
            return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Code Analyzer - Analyze commits with AI')
    parser.add_argument('--test', action='store_true', help='Run setup tests')
    parser.add_argument('--run', action='store_true', help='Run analysis')
    parser.add_argument('--reset-tracking', action='store_true', help='Reset commit tracking')
    
    args = parser.parse_args()
    
    try:
        orchestrator = AICodeAnalyzerOrchestrator()
        
        if args.test:
            logger.info("Running setup tests...")
            results = orchestrator.test_setup()
            print("\n=== Setup Test Results ===")
            for key, value in results.items():
                if isinstance(value, dict):
                    print(f"\n{key}:")
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"{key}: {value}")
        
        elif args.reset_tracking:
            logger.info("Resetting commit tracking...")
            orchestrator.commit_tracker.reset()
            print("✅ Commit tracking reset successfully")
        
        elif args.run or not any([args.test, args.reset_tracking]):
            logger.info("Starting AI code analysis...")
            summary = orchestrator.run()
            print("\n=== Analysis Summary ===")
            for key, value in summary.items():
                print(f"{key}: {value}")
            
            if summary['status'] == 'success':
                print("\n✅ Analysis completed successfully")
            else:
                print("\n❌ Analysis failed")
                sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
