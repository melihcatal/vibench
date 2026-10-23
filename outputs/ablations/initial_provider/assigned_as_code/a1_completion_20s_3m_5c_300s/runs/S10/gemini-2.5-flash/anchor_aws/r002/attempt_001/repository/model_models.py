from typing import Dict, Any

class BedrockRequest:
    def __init__(self, text: str, config: Dict[str, Any] = None):
        self.text = text
        self.config = config if config is not None else {}

class BedrockResponse:
    def __init__(self, text: str):
        self.text = text
