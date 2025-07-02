"""Link validator for Telegram links."""

import re
import logging
import requests
from typing import List, Tuple, Dict
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Container for link validation results."""
    original_link: str
    normalized_link: str
    is_valid: bool
    error_message: str = ""

class LinkValidator:
    """Validates Telegram links."""
    
    # Regex patterns for different link formats
    PATTERNS = {
        'username': r'@([a-zA-Z]\w{3,30}[a-zA-Z\d])',
        't_me': r't\.me/([a-zA-Z]\w{3,30}[a-zA-Z\d])',
        'telegram_me': r'telegram\.me/([a-zA-Z]\w{3,30}[a-zA-Z\d])',
        'https_t_me': r'https://t\.me/([a-zA-Z]\w{3,30}[a-zA-Z\d])',
        'https_telegram_me': r'https://telegram\.me/([a-zA-Z]\w{3,30}[a-zA-Z\d])'
    }
    
    def __init__(self, timeout: float = 0.1):
        """Initialize validator with timeout."""
        self.timeout = timeout
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns."""
        self.compiled_patterns = {
            name: re.compile(pattern)
            for name, pattern in self.PATTERNS.items()
        }
    
    def extract_links(self, text: str) -> List[str]:
        """Extract potential Telegram links from text."""
        links = []
        for pattern in self.compiled_patterns.values():
            links.extend(
                f"@{match}" if not match.startswith(('@', 't', 'h')) else match
                for match in pattern.findall(text)
            )
        return list(set(links))  # Remove duplicates
    
    def normalize_link(self, link: str) -> str:
        """Convert link to standard format (https://t.me/username)."""
        # Extract username from any format
        username = None
        for pattern in self.compiled_patterns.values():
            match = pattern.search(link)
            if match:
                username = match.group(1)
                break
        
        if username:
            return f"https://t.me/{username}"
        return link
    
    def validate_link_format(self, link: str) -> bool:
        """Check if link matches any valid format."""
        return any(
            pattern.fullmatch(link) is not None
            for pattern in self.compiled_patterns.values()
        )
    
    def validate_link_existence(self, link: str) -> Tuple[bool, str]:
        """Check if link points to existing Telegram entity."""
        normalized_link = self.normalize_link(link)
        try:
            response = requests.head(
                normalized_link,
                timeout=self.timeout,
                allow_redirects=True
            )
            return response.status_code == 200, ""
        except requests.Timeout:
            return False, "Request timed out"
        except requests.RequestException as e:
            return False, str(e)
    
    def validate_links(self, text: str) -> Dict[str, ValidationResult]:
        """Extract and validate all links from text."""
        results = {}
        extracted_links = self.extract_links(text)
        
        for link in extracted_links:
            # Validate format
            if not self.validate_link_format(link):
                results[link] = ValidationResult(
                    original_link=link,
                    normalized_link="",
                    is_valid=False,
                    error_message="Invalid link format"
                )
                continue
            
            # Normalize link
            normalized_link = self.normalize_link(link)
            
            # Check existence
            exists, error = self.validate_link_existence(link)
            results[link] = ValidationResult(
                original_link=link,
                normalized_link=normalized_link,
                is_valid=exists,
                error_message=error
            )
        
        return results 