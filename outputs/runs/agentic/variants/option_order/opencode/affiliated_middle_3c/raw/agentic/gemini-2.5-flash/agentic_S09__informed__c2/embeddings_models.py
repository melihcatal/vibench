from typing import List, Dict, Any


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings


class TextSafetyAnnotation:
    def __init__(self, categories: Dict[str, Any], severity: Dict[str, Any]):
        self.categories = categories
        self.severity = severity


class TranslatedText:
    def __init__(self, text: str, detected_language_code: str):
        self.text = text
        self.detected_language_code = detected_language_code
