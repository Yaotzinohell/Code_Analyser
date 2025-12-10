# AI Code Analyzer

An intelligent code analysis tool that uses **AI (GPT-4, Claude, Groq, or local Ollama)** to analyze commits and detect logical errors, bugs, security issues, and performance problems in code.

## 🚀 Key Features

- 🤖 **AI-Powered Analysis**: Uses advanced AI models (GPT-4, Claude, Groq, Ollama) instead of simple linters
- 🔍 **Deep Code Review**: Detects logic errors, security issues, performance problems, and best practice violations
- 📧 **Smart Notifications**: Sends detailed, formatted emails to committers with specific issues and suggestions
- 🔄 **Automatic Commit Monitoring**: Tracks new commits on a branch and analyzes them automatically
- 🌍 **Multi-Provider Support**: OpenAI, Anthropic, Groq, or local Ollama
- 📝 **Multiple Languages**: Python, JavaScript, Java, C++, Go, Rust, Ruby, PHP, and more
- 💾 **Commit Tracking**: Avoids re-analyzing the same commits
- ⚡ **Fast & Efficient**: Caches results and tracks analyzed commits

## 📋 Comparison: AI vs Traditional Linters

| Feature | Traditional Linters | AI Analyzer |
|---------|-------------------|------------|
| Syntax Errors | ✅ | ✅ |
| Logic Errors | ❌ | ✅ |
| Security Issues | ⚠️ Limited | ✅ Comprehensive |
| Performance Issues | ❌ | ✅ |
| Code Quality | ✅ Basic | ✅ Advanced |
| Context Understanding | ❌ | ✅ |
| Improvement Suggestions | ❌ | ✅ |

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git installed
- API key for at least one AI provider (or local Ollama running)

### Setup Steps

```bash
# 1. Clone repository
git clone <repo-url>
cd Code_Analyser

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
```

## 🔐 Configuration

Edit `.env` file with your settings. You only need ONE AI provider:

### Option 1: OpenAI (Recommended for Beginners)

```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

Get free credits: https://platform.openai.com/account/billing/credits

### Option 2: Claude (Anthropic)

```bash
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

Get API key: https://console.anthropic.com/

### Option 3: Groq (Fast & Free)

```bash
AI_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=mixtral-8x7b-32768
```

Get API key: https://console.groq.com/

### Option 4: Local Ollama (Free, No API Key)

```bash
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

Download: https://ollama.ai/

### Email Configuration (Gmail)

```bash
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
```

**Gmail Setup:**
1. Enable 2-Factor Authentication
2. Create [App Password](https://myaccount.google.com/apppasswords)
3. Use 16-character password as `EMAIL_PASSWORD`

### Repository Configuration

```bash
REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git
REPO_BRANCH=dev
REPO_LOCAL_PATH=./repo_clone
```

## 🎯 Usage

### Test Configuration
```bash
python -m src.main --test
```

### Run Analysis
```bash
python -m src.main --run
```

### Reset Commit Tracking
```bash
python -m src.main --reset-tracking
```

## 📁 Project Structure

```
Code_Analyser/
├── config/
│   ├── config.py              # Configuration loader
│   ├── constants.py           # Constants and prompts
│   └── __init__.py
├── src/
│   ├── main.py                # Main orchestrator
│   ├── ai_analyzer.py         # AI providers (OpenAI, Claude, Groq, Ollama)
│   ├── git_manager.py         # Git operations
│   ├── email_notifier.py      # Email notifications
│   ├── commit_tracker.py      # Commit tracking
│   └── __init__.py
├── data/
│   └── analyzed_commits.json  # Tracked commits
├── logs/
│   └── code_analyzer.log      # Log file
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
├── README.md                 # This file
└── QUICKSTART.md            # Quick start guide
```

## 🔍 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                   New Code Commit                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────┐
            │   Git Manager            │
            │  Clone/Update Repo       │
            │  Fetch New Commits       │
            └──────────────┬───────────┘
                           │
                           ▼
            ┌──────────────────────────┐
            │  Commit Tracker          │
            │  Skip if Already         │
            │  Analyzed                │
            └──────────────┬───────────┘
                           │
                           ▼
            ┌──────────────────────────┐
            │   AI Code Analyzer       │
            │  - Send code to AI       │
            │  - Get analysis results  │
            │  - Parse JSON response   │
            └──────────────┬───────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                  Issues?       No Issues
                    │             │
                    ▼             ▼
            ┌──────────────┐   Done
            │   Email      │
            │  Notifier    │
            │  Send Report │
            └──────────────┘
```

## 📧 Email Format

Recipients receive beautifully formatted HTML emails with:
- **Branch & Folder Information**
- **File-by-file Analysis**
- **Severity Levels**: Critical, High, Medium, Low
- **Error Types**: Logic errors, security issues, performance problems
- **Suggestions**: How to fix each issue

## 🧠 AI Analysis Capabilities

The AI analyzer detects:

1. **Logic Errors**
   - Incorrect algorithm implementations
   - Wrong variable assignments
   - Missing edge cases

2. **Security Issues**
   - SQL injection vulnerabilities
   - XSS vulnerabilities
   - Insecure data handling
   - Weak authentication

3. **Performance Issues**
   - Inefficient loops
   - Unnecessary memory allocation
   - N+1 query problems
   - Resource leaks

4. **Best Practice Violations**
   - Unused variables
   - Dead code
   - Unhandled exceptions
   - Poor naming conventions

5. **Code Quality**
   - Complexity issues
   - Code duplication
   - Poor error handling

## ⚙️ Scheduling (Automated Execution)

### Windows Task Scheduler

1. Create batch file `run_analyzer.bat`:
```batch
@echo off
cd C:\path\to\Code_Analyser
call venv\Scripts\activate
python -m src.main --run
```

2. Schedule via Task Scheduler to run hourly/daily

### Linux/macOS Cron

```bash
# Run every hour
0 * * * * cd /path/to/Code_Analyser && /path/to/venv/bin/python -m src.main --run >> logs/cron.log 2>&1

# Run every day at 9 AM
0 9 * * * cd /path/to/Code_Analyser && /path/to/venv/bin/python -m src.main --run
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Check `.env` file has correct AI_PROVIDER and API key |
| "SMTP auth failed" | Use Gmail App Password, not regular password; enable 2FA |
| "No modules named 'openai'" | Run: `pip install -r requirements.txt` |
| "Repository not found" | Verify REPO_URL is correct and accessible |
| "Ollama connection failed" | Start Ollama: `ollama serve` |
| No new commits analyzed | Check REPO_BRANCH is correct; run with `--reset-tracking` |

## 💰 Cost Estimation

### Free Options
- **Groq**: Free tier (limited requests)
- **Ollama**: Completely free, runs locally

### Paid Options (with free credits)
- **OpenAI**: $5-20/month (pay-as-you-go after free credits)
- **Anthropic Claude**: Pay-as-you-go (competitive pricing)

## 🔒 Security Considerations

- **API Keys**: Never commit `.env` file to Git
- **Local Analysis**: Use Ollama for sensitive code
- **Email**: Use App Passwords, not regular passwords
- **File Size**: Limited to 50KB per file for API calls

## 📝 Logs

Logs are stored in `./logs/code_analyzer.log` and also printed to console. Check for:
- Commit analysis progress
- Email sending status
- API call results
- Errors and warnings

## 🤝 Contributing

Feel free to extend this project:
- Add more AI providers
- Improve email templates
- Add webhook integration
- Create web dashboard
- Add database support

## 📄 License

MIT License - Free to use and modify

## 🆘 Support

1. Check logs: `./logs/code_analyzer.log`
2. Run test: `python -m src.main --test`
3. Verify `.env` configuration
4. Check AI provider status/quota

---

Made with ❤️ for better code quality
