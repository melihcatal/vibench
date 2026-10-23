import os
from typing import Dict, Any

class SafetyClient:
    """
    A base client for safety services. Specific implementations will vary by provider.
    """
    def __init__(self, api_key_env_var: str):
        self.api_key = os.environ.get(api_key_env_var)
        if not self.api_key:
            raise ValueError(f"API key not found in environment variable: {api_key_env_var}")

    def moderate(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

    def redact(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

    def embed(self, texts: list[str]) -> Dict[str, Any]:
        raise NotImplementedError

    def translate(self, text: str, target_language: str) -> Dict[str, Any]:
        raise NotImplementedError

    def text_to_speech(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError
