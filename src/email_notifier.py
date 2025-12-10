"""
Email Notifier Module
Sends email notifications to committers
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class EmailNotifier:
    def __init__(self, sender: str, password: str, smtp_server: str = 'smtp.gmail.com', smtp_port: int = 587):
        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_error_notification(self, recipient_email: str, author_name: str, branch: str,
                               folder_name: str, analysis_results: dict) -> bool:
        """Send email notification about code errors"""
        try:
            subject = f"[Code Analyzer] Issues found in {branch} branch - {folder_name}"
            body = self._build_email_body(author_name, branch, folder_name, analysis_results)
            
            message = MIMEMultipart()
            message['From'] = self.sender
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(message)
            
            logger.info(f"Email sent to {recipient_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check EMAIL_SENDER and EMAIL_PASSWORD.")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _build_email_body(self, author_name: str, branch: str, folder_name: str, analysis_results: dict) -> str:
        """Build HTML email body"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .container {{ max-width: 800px; margin: 0 auto; }}
                    .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .section {{ margin: 20px 0; padding: 15px; background-color: white; border-radius: 5px; }}
                    .error-critical {{ border-left: 5px solid #d32f2f; }}
                    .error-high {{ border-left: 5px solid #f57c00; }}
                    .error-medium {{ border-left: 5px solid #fbc02d; }}
                    .error-low {{ border-left: 5px solid #388e3c; }}
                    .file-name {{ font-weight: bold; color: #1976d2; margin-top: 10px; }}
                    .error-list {{ margin: 10px 0; padding-left: 20px; }}
                    .error-item {{ margin: 10px 0; padding: 10px; background-color: #f5f5f5; border-radius: 3px; }}
                    .severity {{ font-weight: bold; padding: 2px 8px; border-radius: 3px; display: inline-block; }}
                    .severity-critical {{ background-color: #d32f2f; color: white; }}
                    .severity-high {{ background-color: #f57c00; color: white; }}
                    .severity-medium {{ background-color: #fbc02d; color: black; }}
                    .severity-low {{ background-color: #388e3c; color: white; }}
                    .footer {{ color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⚠️ Code Analysis Issues Detected</h1>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{author_name}</strong>,</p>
                        <p>AI code analysis has detected issues in your recent commit:</p>
                        
                        <div class="section">
                            <p><strong>🌳 Branch:</strong> {branch}</p>
                            <p><strong>📁 Folder:</strong> {folder_name}</p>
                            <p><strong>🔍 Analysis Tool:</strong> AI Code Analyzer (Powered by GPT/Claude)</p>
                        </div>
        """
        
        # Add file-specific errors
        if 'files' in analysis_results:
            for file_result in analysis_results['files']:
                if file_result.get('errors') or file_result.get('has_errors'):
                    html += f"""
                        <div class="section error-{file_result.get('severity', 'low')}">
                            <div class="file-name">📄 {file_result.get('file', 'Unknown')}</div>
                            <p><strong>Language:</strong> {file_result.get('language', 'Unknown')}</p>
                    """
                    
                    if file_result.get('errors'):
                        html += '<div class="error-list">'
                        for error in file_result['errors']:
                            if isinstance(error, dict):
                                line = error.get('line', 'N/A')
                                msg = error.get('message', '')
                                severity = error.get('severity', 'medium').lower()
                                error_type = error.get('type', 'unknown')
                                suggestion = error.get('suggestion', '')
                                
                                html += f"""
                                    <div class="error-item">
                                        <span class="severity severity-{severity}">{severity.upper()}</span>
                                        <strong>{error_type.replace('_', ' ').title()}</strong>
                                        {f'(Line {line})' if line != 'N/A' else ''}<br>
                                        <p>{msg}</p>
                                        {f'<p><em>💡 Suggestion: {suggestion}</em></p>' if suggestion else ''}
                                    </div>
                                """
                        html += '</div>'
                    
                    if file_result.get('summary'):
                        html += f'<p><strong>Summary:</strong> {file_result["summary"]}</p>'
                    
                    html += '</div>'
        
        html += """
                        <div class="section">
                            <p>👉 <strong>Next Steps:</strong></p>
                            <ul>
                                <li>Review the issues listed above</li>
                                <li>Make the necessary fixes in your code</li>
                                <li>Commit and push the corrected code</li>
                                <li>The analyzer will re-check on your next commit</li>
                            </ul>
                        </div>
                        
                        <div class="footer">
                            <p>This is an automated message from AI Code Analyzer. Please do not reply to this email.</p>
                            <p>For questions or to disable notifications, contact your project administrator.</p>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html
    
    def test_email_configuration(self) -> bool:
        """Test if email configuration is correct"""
        try:
            message = MIMEMultipart()
            message['From'] = self.sender
            message['To'] = self.sender
            message['Subject'] = '[Code Analyzer] Test Email'
            message.attach(MIMEText('<p>Test email from Code Analyzer. Configuration is working!</p>', 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(message)
            
            logger.info("Test email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Test email failed: {str(e)}")
            return False
