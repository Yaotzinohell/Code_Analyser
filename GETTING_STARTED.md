# Getting Started

## 🎯 Project Overview

This is an **AI-powered Code Analyzer** that:
1. 🔍 Monitors Git commits on a specific branch
2. 🤖 Analyzes code using AI (GPT-4, Claude, Groq, or local Ollama)
3. 📧 Sends intelligent email reports to committers with specific issues and suggestions

## 📦 What's Included

```
src/
├── main.py              - Main orchestrator (run this)
├── ai_analyzer.py       - AI providers (OpenAI, Claude, Groq, Ollama)
├── git_manager.py       - Git operations
├── email_notifier.py    - Email notifications  
└── commit_tracker.py    - Commit tracking

config/
├── config.py            - Load configuration from .env
└── constants.py         - AI prompt and constants

data/                    - Persistent data (analyzed commits)
logs/                    - Application logs
```

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get an AI API Key
Choose ONE:
- **OpenAI**: https://platform.openai.com/api-keys
- **Groq (Free)**: https://console.groq.com/
- **Claude**: https://console.anthropic.com/
- **Ollama (Local)**: https://ollama.ai/

### 3. Configure
```bash
copy .env.example .env
# Edit .env with your AI provider and Gmail settings
```

### 4. Test
```bash
python -m src.main --test
```

### 5. Analyze
```bash
python -m src.main --run
```

## 📚 Documentation Files

- **README.md** - Full documentation with examples
- **QUICKSTART.md** - 5-minute setup guide  
- **ENV_GUIDE.md** - All environment variables explained

## 🤖 AI Capabilities

Your analyzer detects:
- ✅ Logic errors and bugs
- ✅ Security vulnerabilities
- ✅ Performance issues
- ✅ Best practice violations
- ✅ Code quality problems

With intelligent suggestions for fixing each issue!

## 💡 Example Workflow

```
1. Developer commits code to 'dev' branch
2. Analyzer detects new commit
3. AI analyzes the code
4. Issues found? Email sent!
5. Developer gets detailed report with suggestions
```

## ⚙️ Configuration

### Minimal .env
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...

REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git
REPO_BRANCH=dev

EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

See `ENV_GUIDE.md` for all options.

## 📝 Common Commands

```bash
# Run analysis (clone repo, analyze commits, send emails)
python -m src.main --run

# Test configuration (email, AI, repository)
python -m src.main --test

# Reset tracking (re-analyze all commits)
python -m src.main --reset-tracking

# View logs
type logs\code_analyzer.log
```

## 🆘 Need Help?

1. **Check logs**: `logs/code_analyzer.log`
2. **Run tests**: `python -m src.main --test`
3. **Read docs**: `README.md`, `QUICKSTART.md`, `ENV_GUIDE.md`
4. **Verify .env**: Make sure all required variables are set

## 🎓 Learning Path

1. Read this file first ✅
2. Follow `QUICKSTART.md` to get running
3. Check `README.md` for detailed features
4. Check `ENV_GUIDE.md` for all configuration options
5. Explore source code in `src/`

## 🔄 Automation

To run this automatically:

**Windows Task Scheduler**
- Create a batch file that runs: `python -m src.main --run`
- Schedule it to run hourly/daily

**Linux Cron**
```bash
0 * * * * cd /path/to/Code_Analyser && /path/to/venv/bin/python -m src.main --run
```

## 💰 Costs

- **OpenAI**: $5 free credits → ~$0.30-0.50/analysis
- **Groq**: Free tier available
- **Claude**: Pay-as-you-go
- **Ollama**: Completely free (local)

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Get an AI API key
3. ✅ Configure `.env`
4. ✅ Run `python -m src.main --test`
5. ✅ Run `python -m src.main --run`
6. ✅ Check your email! 📧

---

**Questions?** Check the documentation files or review the source code!

**Ready?** Start with: `python -m src.main --test`
