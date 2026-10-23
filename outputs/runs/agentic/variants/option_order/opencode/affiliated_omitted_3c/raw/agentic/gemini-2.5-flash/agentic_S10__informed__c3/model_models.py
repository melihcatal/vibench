from typing import List, Dict, Any


class LLMRequest:
    def __init__(self, prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 150):
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens


class LLMResponse:
    def __init__(self, text: str, model: str, usage: Dict[str, Any]):
        self.text = text
        self.model = model
        self.usage = usage


class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class ModerationResult:
    def __init__(
        self,
        categories: Dict[str, bool],
        category_scores: Dict[str, float],
        flagged: bool,
    ):
        self.categories = categories
        self.category_scores = category_scores
        self.flagged = flagged


class TranslationResult:
    def __init__(self, translated_text: str, detected_source_lang: str):
        self.translated_text = translated_text
        self.detected_source_lang = detected_source_lang


class EmbeddingResult:
    def __init__(self, embedding: List[float], model: str):
        self.embedding = embedding
        self.model = model


class SpeechResult:
    def __init__(self, audio_content: bytes, synthesis_time: float):
        self.audio_content = audio_content
        self.synthesis_time = synthesis_time
