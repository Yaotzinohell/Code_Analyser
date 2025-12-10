"""
AI Code Analyzer Module
Uses Claude, GPT, Groq, or Ollama to analyze code
"""
import os
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class AICodeAnalyzer:
    """Abstract base class for AI code analyzers"""
    
    def __init__(self):
        self.supported_languages = {
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
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a single file"""
        raise NotImplementedError
    
    def _read_file_content(self, file_path: str, max_size: int = 50000) -> Optional[str]:
        """Read file content with size limit"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return None
            
            file_size = os.path.getsize(file_path)
            if file_size > max_size:
                logger.warning(f"File too large ({file_size} bytes): {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return None
    
    def _get_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix
        return self.supported_languages.get(ext)


class OpenAIAnalyzer(AICodeAnalyzer):
    """OpenAI GPT-based code analyzer"""
    
    def __init__(self, api_key: str, model: str = 'gpt-4o-mini'):
        super().__init__()
        self.api_key = api_key
        self.model = model
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            logger.error("openai package not installed. Install with: pip install openai")
            self.client = None
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze code file using OpenAI"""
        try:
            if not self.client:
                return {'file': file_path, 'error': 'OpenAI client not initialized'}
            
            code_content = self._read_file_content(file_path)
            if not code_content:
                return {'file': file_path, 'error': 'Could not read file'}
            
            language = self._get_language(file_path)
            if not language:
                return {'file': file_path, 'error': 'Unsupported language'}
            
            # Build prompt
            from config.constants import AI_CODE_ANALYSIS_PROMPT
            prompt = AI_CODE_ANALYSIS_PROMPT.format(
                language=language,
                code=code_content,
                file_path=file_path
            )
            
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=60
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content
            
            # Extract JSON from response
            analysis = self._parse_analysis(analysis_text)
            analysis['file'] = file_path
            analysis['language'] = language
            
            logger.info(f"Analyzed {file_path} with OpenAI")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {'file': file_path, 'error': str(e)}
    
    def _parse_analysis(self, response_text: str) -> Dict:
        """Extract JSON from AI response"""
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'has_errors': False, 'summary': response_text}
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON response")
            return {'has_errors': False, 'summary': response_text}


class AnthropicAnalyzer(AICodeAnalyzer):
    """Anthropic Claude-based code analyzer"""
    
    def __init__(self, api_key: str, model: str = 'claude-3-5-sonnet-20241022'):
        super().__init__()
        self.api_key = api_key
        self.model = model
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            logger.error("anthropic package not installed. Install with: pip install anthropic")
            self.client = None
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze code file using Claude"""
        try:
            if not self.client:
                return {'file': file_path, 'error': 'Claude client not initialized'}
            
            code_content = self._read_file_content(file_path)
            if not code_content:
                return {'file': file_path, 'error': 'Could not read file'}
            
            language = self._get_language(file_path)
            if not language:
                return {'file': file_path, 'error': 'Unsupported language'}
            
            # Build prompt
            from config.constants import AI_CODE_ANALYSIS_PROMPT
            prompt = AI_CODE_ANALYSIS_PROMPT.format(
                language=language,
                code=code_content,
                file_path=file_path
            )
            
            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=60
            )
            
            # Parse response
            analysis_text = response.content[0].text
            analysis = self._parse_analysis(analysis_text)
            analysis['file'] = file_path
            analysis['language'] = language
            
            logger.info(f"Analyzed {file_path} with Claude")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {'file': file_path, 'error': str(e)}
    
    def _parse_analysis(self, response_text: str) -> Dict:
        """Extract JSON from AI response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'has_errors': False, 'summary': response_text}
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON response")
            return {'has_errors': False, 'summary': response_text}


class GroqAnalyzer(AICodeAnalyzer):
    """Groq-based code analyzer (fast inference)"""
    
    def __init__(self, api_key: str, model: str = 'mixtral-8x7b-32768'):
        super().__init__()
        self.api_key = api_key
        self.model = model
        
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
        except ImportError:
            logger.error("groq package not installed. Install with: pip install groq")
            self.client = None
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze code file using Groq"""
        try:
            if not self.client:
                return {'file': file_path, 'error': 'Groq client not initialized'}
            
            code_content = self._read_file_content(file_path)
            if not code_content:
                return {'file': file_path, 'error': 'Could not read file'}
            
            language = self._get_language(file_path)
            if not language:
                return {'file': file_path, 'error': 'Unsupported language'}
            
            # Build prompt
            from config.constants import AI_CODE_ANALYSIS_PROMPT
            prompt = AI_CODE_ANALYSIS_PROMPT.format(
                language=language,
                code=code_content,
                file_path=file_path
            )
            
            # Call Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=60
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content
            analysis = self._parse_analysis(analysis_text)
            analysis['file'] = file_path
            analysis['language'] = language
            
            logger.info(f"Analyzed {file_path} with Groq")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {'file': file_path, 'error': str(e)}
    
    def _parse_analysis(self, response_text: str) -> Dict:
        """Extract JSON from AI response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'has_errors': False, 'summary': response_text}
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON response")
            return {'has_errors': False, 'summary': response_text}


class OllamaAnalyzer(AICodeAnalyzer):
    """Ollama-based local code analyzer (free, runs locally)"""
    
    def __init__(self, base_url: str = 'http://localhost:11434', model: str = 'mistral'):
        super().__init__()
        self.base_url = base_url
        self.model = model
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            logger.error("requests package not installed. Install with: pip install requests")
            self.requests = None
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze code file using local Ollama"""
        try:
            if not self.requests:
                return {'file': file_path, 'error': 'Requests library not available'}
            
            code_content = self._read_file_content(file_path)
            if not code_content:
                return {'file': file_path, 'error': 'Could not read file'}
            
            language = self._get_language(file_path)
            if not language:
                return {'file': file_path, 'error': 'Unsupported language'}
            
            # Build prompt
            from config.constants import AI_CODE_ANALYSIS_PROMPT
            prompt = AI_CODE_ANALYSIS_PROMPT.format(
                language=language,
                code=code_content,
                file_path=file_path
            )
            
            # Call Ollama
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3
                },
                timeout=60
            )
            
            if response.status_code != 200:
                return {'file': file_path, 'error': f'Ollama error: {response.status_code}'}
            
            # Parse response
            response_data = response.json()
            analysis_text = response_data.get('response', '')
            analysis = self._parse_analysis(analysis_text)
            analysis['file'] = file_path
            analysis['language'] = language
            
            logger.info(f"Analyzed {file_path} with Ollama")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {'file': file_path, 'error': str(e)}
    
    def _parse_analysis(self, response_text: str) -> Dict:
        """Extract JSON from AI response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'has_errors': False, 'summary': response_text}
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON response")
            return {'has_errors': False, 'summary': response_text}


def get_analyzer(provider: str = 'openai', **kwargs) -> AICodeAnalyzer:
    """Factory function to get appropriate analyzer"""
    provider = provider.lower()
    
    if provider == 'openai':
        api_key = kwargs.get('api_key') or os.getenv('OPENAI_API_KEY')
        model = kwargs.get('model') or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        return OpenAIAnalyzer(api_key, model)
    
    elif provider == 'anthropic':
        api_key = kwargs.get('api_key') or os.getenv('ANTHROPIC_API_KEY')
        model = kwargs.get('model') or os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
        return AnthropicAnalyzer(api_key, model)
    
    elif provider == 'groq':
        api_key = kwargs.get('api_key') or os.getenv('GROQ_API_KEY')
        model = kwargs.get('model') or os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')
        return GroqAnalyzer(api_key, model)
    
    elif provider == 'ollama':
        base_url = kwargs.get('base_url') or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        model = kwargs.get('model') or os.getenv('OLLAMA_MODEL', 'mistral')
        return OllamaAnalyzer(base_url, model)
    
    else:
        raise ValueError(f"Unknown AI provider: {provider}")
