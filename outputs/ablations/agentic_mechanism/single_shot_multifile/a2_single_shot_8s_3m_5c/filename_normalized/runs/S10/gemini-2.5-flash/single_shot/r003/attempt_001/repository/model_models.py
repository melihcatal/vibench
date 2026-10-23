from typing import List, Dict, Any, Optional

class LLMRequest:
    def __init__(self, prompt: str, model_id: str, max_tokens: int = 1024, temperature: float = 0.7, **kwargs):
        self.prompt = prompt
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

class LLMResponse:
    def __init__(self, text: str, model_id: str, **kwargs):
        self.text = text
        self.model_id = model_id
        self.kwargs = kwargs

class ContextAnswerRequest(LLMRequest):
    def __init__(self, prompt: str, context: str, model_id: str, max_tokens: int = 1024, temperature: float = 0.7, **kwargs):
        super().__init__(prompt=prompt, model_id=model_id, max_tokens=max_tokens, temperature=temperature, **kwargs)
        self.context = context

class ExtractedJSONResponse(LLMResponse):
    def __init__(self, json_content: Dict[str, Any], model_id: str, raw_text: str = "", **kwargs):
        super().__init__(text=raw_text, model_id=model_id, **kwargs)
        self.json_content = json_content

class StreamCompletionChunk:
    def __init__(self, delta: str, finish_reason: Optional[str] = None, **kwargs):
        self.delta = delta
        self.finish_reason = finish_reason
        self.kwargs = kwargs

class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text

class SafetyCheckResult:
    def __init__(self, safe: bool, reasons: List[str]):
        self.safe = safe
        self.reasons = reasons

class TranslationRequest:
    def __init__(self, text: str, target_language: str, source_language: Optional[str] = None):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language

class TranslatedTextResponse:
    def __init__(self, translated_text: str, detected_source_language: Optional[str] = None):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

class SpokenBriefRequest:
    def __init__(self, text: str, voice_name: str = "en-US-Standard-C"):
        self.text = text
        self.voice_name = voice_name

class SpokenBriefResponse:
    def __init__(self, audio_content: bytes, audio_format: str = "LINEAR16"):
        self.audio_content = audio_content
        self.audio_format = audio_format