# Environment Variables Guide

## AI Provider Configuration

Choose ONE of the following AI providers:

### OpenAI (GPT-4o-mini recommended)
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

**Cost**: ~$0.10-0.30 per analysis
**Speed**: Medium
**Quality**: Excellent
**Get Key**: https://platform.openai.com/api-keys

### Anthropic Claude
```
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Cost**: Pay-as-you-go
**Speed**: Medium
**Quality**: Excellent
**Get Key**: https://console.anthropic.com/

### Groq (Mixtral - Fast & Free)
```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=mixtral-8x7b-32768
```

**Cost**: Free tier available
**Speed**: Fast (3x faster than others)
**Quality**: Good
**Get Key**: https://console.groq.com/

### Ollama (Local, Free)
```
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

**Cost**: Free
**Speed**: Depends on hardware
**Quality**: Good
**Get**: https://ollama.ai/

---

## Repository Configuration

```
# The GitHub repository to analyze
REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git

# Branch to monitor for new commits
REPO_BRANCH=dev

# Where to clone the repository locally
REPO_LOCAL_PATH=./repo_clone
```

---

## Email Configuration (Gmail Required)

```
# Your Gmail address
EMAIL_SENDER=your_email@gmail.com

# Gmail App Password (NOT your regular password!)
# Get from: https://myaccount.google.com/apppasswords
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

# SMTP server (Gmail)
EMAIL_SMTP_SERVER=smtp.gmail.com

# SMTP port
EMAIL_SMTP_PORT=587
```

### How to Get Gmail App Password:

1. Go to https://myaccount.google.com/apppasswords
2. Sign in with your Google account
3. Select "Mail" and "Windows Computer"
4. Click "Generate"
5. Copy the 16-character password
6. Paste in `.env` as `EMAIL_PASSWORD`

---

## Logging Configuration

```
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Where to save logs
LOG_FILE=./logs/code_analyzer.log
```

---

## File Tracking Configuration

```
# Where to store analyzed commit hashes
# Prevents re-analyzing the same commits
TRACKED_COMMITS_FILE=./data/analyzed_commits.json
```

---

## Analysis Configuration

```
# Whether to analyze qn.txt files
CHECK_QN_FILE=false

# Maximum file size to analyze (in bytes)
# Large files skipped for performance
MAX_FILE_SIZE_BYTES=50000

# Timeout for AI analysis (in seconds)
AI_TIMEOUT_SECONDS=60
```

---

## Example .env Files

### Option 1: OpenAI Setup
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-abc123...
OPENAI_MODEL=gpt-4o-mini

REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git
REPO_BRANCH=dev

EMAIL_SENDER=myemail@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

LOG_LEVEL=INFO
```

### Option 2: Groq Setup (Free)
```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_abc123...
GROQ_MODEL=mixtral-8x7b-32768

REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git
REPO_BRANCH=dev

EMAIL_SENDER=myemail@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

LOG_LEVEL=INFO
```

### Option 3: Local Ollama (Free)
```
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

REPO_URL=https://github.com/Yaotzinohell/LEETCODE_Solutions.git
REPO_BRANCH=dev

EMAIL_SENDER=myemail@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

LOG_LEVEL=INFO
```

---

## Supported Environments

- ✅ Windows (with Python 3.8+)
- ✅ macOS (with Python 3.8+)
- ✅ Linux (with Python 3.8+)
- ✅ Docker containers
