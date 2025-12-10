# Quick Start Guide - 5 Minutes to AI Code Analysis

## 1️⃣ Setup (2 minutes)

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2️⃣ Get an AI API Key (1 minute)

Choose ONE option:

**Option A: OpenAI (Easiest)**
- Go to https://platform.openai.com/account/billing/credits
- Copy your API key

**Option B: Groq (Free & Fast)**
- Go to https://console.groq.com/
- Sign up and get API key

**Option C: Ollama (Free, Local)**
- Download from https://ollama.ai/
- Run `ollama serve`
- Run `ollama pull mistral`

**Option D: Claude (Anthropic)**
- Go to https://console.anthropic.com/
- Copy your API key

## 3️⃣ Configure (1 minute)

```bash
# Copy template
copy .env.example .env
```

Edit `.env` with your choices:

```bash
# Choose your AI provider
AI_PROVIDER=openai  # or anthropic, groq, ollama

# If OpenAI
OPENAI_API_KEY=sk-...

# Email settings (Gmail)
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# Repository
REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git
REPO_BRANCH=dev
```

**Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"  
3. Copy the 16-character password

## 4️⃣ Test Setup (1 minute)

```bash
python -m src.main --test
```

Expected output:
```
=== Setup Test Results ===
ai_configured: True
email_configured: True
repo_accessible: True
```

## 5️⃣ Run Analysis! 🎉

```bash
python -m src.main --run
```

That's it! The analyzer will:
1. ✅ Clone the repository
2. ✅ Find new commits
3. ✅ Analyze code with AI
4. ✅ Send emails if issues found

## 📧 What You'll Get

An email from each committer's repository like:

```
Subject: [Code Analyzer] Issues found in dev branch - LeetcodeFolder

Content:
⚠️ Code Analysis Issues Detected

Branch: dev
Folder: LeetcodeFolder

📄 solution.py (Language: python)

🔴 CRITICAL - Logic Error (Line 42)
   The algorithm returns incorrect results for edge cases
   💡 Suggestion: Add check for empty input

🟠 HIGH - Performance Issue (Line 78)  
   O(n²) complexity can be optimized to O(n log n)
   💡 Suggestion: Use sorting instead of nested loops
```

## 🔧 Common Commands

```bash
# Run analysis
python -m src.main --run

# Test everything is working
python -m src.main --test

# Reset analyzed commits (re-analyze all)
python -m src.main --reset-tracking
```

## ⚡ What's Different from Regular Linters

| Feature | Regular Linters | AI Analyzer |
|---------|----------------|------------|
| Finds syntax errors | ✅ | ✅ |
| Finds logic bugs | ❌ | ✅ |
| Finds security issues | ⚠️ | ✅ |
| Gives improvement suggestions | ❌ | ✅ |
| Understands context | ❌ | ✅ |

## 🆘 Troubleshooting

**"SMTP authentication failed"**
- Use Gmail App Password, NOT your regular password
- Make sure 2FA is enabled

**"No API key found"**
- Check `.env` file exists in project root
- Check you have the right variable name

**"Connection refused for Ollama"**
- Make sure Ollama is running: `ollama serve`
- Make sure you downloaded a model: `ollama pull mistral`

**"No new commits found"**
- Check `REPO_BRANCH` is correct in `.env`
- Run `python -m src.main --reset-tracking` to re-analyze

## 📊 Cost

- **OpenAI**: ~$0.10-0.50 per analysis (with free $5 credit)
- **Groq**: Free tier available
- **Ollama**: Completely free
- **Claude**: Pay-as-you-go

## 🚀 Next Steps

1. Set up Windows Task Scheduler for automatic hourly runs
2. Customize email templates in `src/email_notifier.py`
3. Add more repositories by creating multiple configurations
4. Set up GitHub webhooks for real-time analysis

---

For detailed info, see `README.md`
