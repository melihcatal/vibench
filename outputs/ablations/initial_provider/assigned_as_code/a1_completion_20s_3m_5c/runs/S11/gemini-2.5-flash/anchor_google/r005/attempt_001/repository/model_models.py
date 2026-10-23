from typing import Dict, Any, List

class ModelRequest:
    def __init__(self, text: str, config: Dict[str, Any] = None):
        self.text = text
        self.config = config or {}

class ModelResponse:
    def __init__(self, text: str, metadata: Dict[str, Any] = None):
        self.text = text
        self.metadata = metadata or {}

class SafetyRating:
    def __init__(self, category: str, probability: str):
        self.category = category
        self.probability = probability

class LocalizedOutput:
    def __init__(self, text: str, language_code: str):
        self.text = text
        self.language_code = language_code

class EmbeddingOutput:
    def __init__(self, values: List[float]):
        self.values = values
