"""
Constants for AI Code Analyzer
"""

# AI Analysis Prompt
AI_CODE_ANALYSIS_PROMPT = """You are an expert code reviewer. Analyze the following code and identify:
1. Logic errors or potential bugs
2. Performance issues
3. Security vulnerabilities
4. Code quality problems
5. Best practice violations

Code:
```{language}
{code}
```

File: {file_path}
Language: {language}

Provide a detailed analysis in JSON format with this structure:
{{
    "has_errors": boolean,
    "severity": "critical" | "high" | "medium" | "low" | "none",
    "errors": [
        {{
            "line": number or null,
            "type": string (e.g., "logic_error", "security_issue", "performance", "best_practice"),
            "severity": "critical" | "high" | "medium" | "low",
            "message": string,
            "suggestion": string
        }}
    ],
    "summary": string
}}

Be thorough but concise. Focus on actual issues, not stylistic preferences."""

# Error Severity Levels
SEVERITY_CRITICAL = 'critical'
SEVERITY_HIGH = 'high'
SEVERITY_MEDIUM = 'medium'
SEVERITY_LOW = 'low'
SEVERITY_NONE = 'none'

# Error Types
ERROR_TYPE_LOGIC = 'logic_error'
ERROR_TYPE_SECURITY = 'security_issue'
ERROR_TYPE_PERFORMANCE = 'performance'
ERROR_TYPE_BEST_PRACTICE = 'best_practice'
ERROR_TYPE_SYNTAX = 'syntax_error'

# File Patterns
QN_FILE_PATTERN = 'qn.txt'
SOLUTION_FILE_PATTERN = 'solution.'

# Email Subject Templates
EMAIL_SUBJECT_TEMPLATE = '[Code Analyzer] Issues found in {branch} branch - {folder_name}'

# Timeouts
GIT_CLONE_TIMEOUT = 300
AI_ANALYSIS_TIMEOUT = 60

# Commit Tracking
COMMIT_TRACKING_VERSION = 1
