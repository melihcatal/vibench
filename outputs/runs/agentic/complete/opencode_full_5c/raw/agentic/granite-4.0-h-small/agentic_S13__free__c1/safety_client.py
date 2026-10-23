```python
# safety_client.py
# HELPER: Provide local configuration and client helper utilities for Text Content Safety

import os
import json
from typing import Any, Dict

# Example: load a JSON config that holds provider credentials
CONFIG_PATH = os.getenv('SAFETY_CONFIG_PATH', '/app/config/safety.json')

def load_config() -> Dict[str, Any]:
    """Load provider configuration (API key, endpoint, model ID)."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Default in‑code config for demo purposes
    return {
        'api_key': os.getenv('SAFETY_API_KEY', 'demo_key'),
        'base_url': os.getenv('SAFETY_BASE_URL', 'https://api.demo.provider.com'),
        'model_id': os.getenv('SAFETY_MODEL_ID', 'text-safety-v1')
    }

def get_client_config() -> Dict[str, Any]:
    """Return a dict suitable for initializing the external SDK or HTTP client."""
    cfg = load_config()
    return {
        'api_key': cfg['api_key'],
        'endpoint': cfg['base_url'],
        'model': cfg['model_id']
    }

# Example generic SDK usage (replace with real SDK if needed)
class SafetyClient:
    """Thin wrapper around the external Text Content Safety service."""
    def __init__(self):
        cfg = get_client_config()
        # Placeholder: assume the provider SDK is imported here
        from provider_sdk import TextSafetyService  # type: ignore
        self.service = TextSafetyService(**cfg)
    
    def analyze_text(self, text: str) -> dict:
        """Send a single text and return raw provider response."""
        return self.service.analyze(text)
    
    def analyze_batch(self, texts: list[str]) -> list[dict]:
        """Batch version of analyze_text."""
        return self.service.analyze_batch(texts)
    
    def detect_unsafe_spans(self, text: str) -> list[dict]:
        """Return list of unsafe span dicts from provider."""
        return self.service.detect_spans(text)
```