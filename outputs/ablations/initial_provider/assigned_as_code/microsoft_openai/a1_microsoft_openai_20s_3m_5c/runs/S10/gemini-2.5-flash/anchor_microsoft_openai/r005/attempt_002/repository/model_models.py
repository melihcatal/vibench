from typing import Dict, Any, List

class LLMRequest:
    def __init__(self, model: str, messages: List[Dict[str, str]], **kwargs):
        self.model = model
        self.messages = messages
        self.kwargs = kwargs

class LLMResponse:
    def __init__(self, content: str, **kwargs):
        self.content = content
        self.kwargs = kwargs
