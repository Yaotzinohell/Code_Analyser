"""
Configuration for AI-powered Code Analyzer
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Repository Configuration
REPO_URL = os.getenv('REPO_URL', 'https://github.com/Yaotzinohell/LEETCODE_Solutions.git')
REPO_BRANCH = os.getenv('REPO_BRANCH', 'dev')
REPO_LOCAL_PATH = os.getenv('REPO_LOCAL_PATH', './repo_clone')

# AI Provider Configuration
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # 'openai', 'anthropic', 'groq', 'ollama'

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # or gpt-3.5-turbo for cheaper option

# Anthropic Configuration (Claude)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')

# Groq Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')

# Ollama Configuration (Local)
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

# Email Configuration
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', 587))

# Analysis Configuration
SUPPORTED_LANGUAGES = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.go': 'go',
    '.rs': 'rust',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift'
}

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/code_analyzer.log')

# Tracking Configuration
TRACKED_COMMITS_FILE = os.getenv('TRACKED_COMMITS_FILE', './data/analyzed_commits.json')

# Analysis Configuration
CHECK_QN_FILE = os.getenv('CHECK_QN_FILE', 'false').lower() == 'true'
MAX_FILE_SIZE_BYTES = int(os.getenv('MAX_FILE_SIZE_BYTES', 50000))  # 50KB limit for AI analysis
AI_TIMEOUT_SECONDS = int(os.getenv('AI_TIMEOUT_SECONDS', 60))
