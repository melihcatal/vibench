import os
from dashscope import SpeechRecognizer
from typing import Optional

class DashScopeSpeechClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        
    def get_recognizer(self, **kwargs) -> SpeechRecognizer:
        return SpeechRecognizer(**kwargs)

def get_dashscope_client() -> DashScopeSpeechClient:
    return DashScopeSpeechClient()