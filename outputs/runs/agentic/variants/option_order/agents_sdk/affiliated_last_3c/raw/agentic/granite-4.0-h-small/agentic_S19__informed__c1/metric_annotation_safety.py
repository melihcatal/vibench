# [LATER-STEP] metric_annotation_safety.py

import re
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.identity import DefaultAzureCredential

# Environment variable pointing to Azure Content Safety endpoint
CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

_conn = None

def _get_content_safety_client() -> ContentSafetyClient:
    global _conn
    if _conn is None:
        _conn = ContentSafetyClient(endpoint=CONTENT_SAFETY_ENDPOINT,
                                     credential=DefaultAzureCredential())
    return _conn

SAFE_KEYWORDS = {'error', 'fail', 'exception', 'null', 'undefined'}

SAFE_REGEXES = [re.compile(r'\b(?:error|fail|exception)\b', re.IGNORECASE),
                re.compile(r'null', re.IGNORECASE),
                re.compile(r'undefined', re.IGNORECASE)]

def is_safe(annotation: str) -> bool:
    """Check free-text metric label/annotation for unsafe or potentially harmful content.
    Uses Azure Content Safety (moderation) API first, then fallback to simple regex checks.
    Returns True if safe, False otherwise.
    """
    client = _get_content_safety_client()
    result = client.analyze_text(content=annotation)
    # Azure Content Safety returns categories like 'hate', 'selfHarm', etc.
    unsafe = any(getattr(result, cat, False) for cat in ['hate', 'selfHarm', 'sexual', 'violence'])
    if not unsafe:
        # Fallback simple heuristics
        for regex in SAFE_REGEXES:
            if regex.search(annotation):
                return False
        for word in SAFE_KEYWORDS:
            if word in annotation.lower():
                return False
    return True