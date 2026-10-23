from typing import Optional, Dict, Any

class ModelRequest:
    def __init__(self, prompt: str, model: str = "gpt-4o", temperature: float = 0.7):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature

class ModelResponse:
    def __init__(self, content: str, model_id: str, usage: Optional[Dict[str, Any]] = None):
        self.content = content
        self.model_id = model_id
        self.usage = usage

    def normalize(self):
        return {
            "text": self.content,
            "model": self.model_id,
            "token_usage": self.usage
        }
