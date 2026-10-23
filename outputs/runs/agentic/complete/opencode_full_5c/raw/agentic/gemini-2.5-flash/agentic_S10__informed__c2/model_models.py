import json
from typing import Any, Dict, List, Optional, Union


class ChatPrompt:
    def __init__(self, role: str, parts: List[Union[str, Dict]]):
        self.role = role
        self.parts = parts

    def to_gemini_format(self):
        return {
            "role": self.role,
            "parts": [
                {"text": part} if isinstance(part, str) else part for part in self.parts
            ],
        }


class TextCompletionRequest:
    def __init__(
        self,
        prompt: str,
        model_name: str = "gemini-pro",
        max_output_tokens: int = 1000,
        temperature: float = 0.7,
    ):
        self.prompt = prompt
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature


class ChatCompletionRequest:
    def __init__(
        self,
        history: List[ChatPrompt],
        model_name: str = "gemini-pro",
        max_output_tokens: int = 1000,
        temperature: float = 0.7,
    ):
        self.history = history
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature


class EmbeddingRequest:
    def __init__(self, text: Union[str, List[str]], model_name: str = "embedding-001"):
        self.text = text
        self.model_name = model_name


class LLMResponse:
    def __init__(
        self,
        text: Optional[str] = None,
        json_data: Optional[Dict] = None,
        finish_reason: Optional[str] = None,
    ):
        self.text = text
        self.json_data = json_data
        self.finish_reason = finish_reason

    @classmethod
    def from_gemini_response(cls, response: Any):
        text = None
        json_data = None
        finish_reason = None

        if response and hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                text_parts = [
                    part.text
                    for part in candidate.content.parts
                    if hasattr(part, "text")
                ]
                text = " ".join(text_parts)

                try:
                    # Attempt to parse as JSON if it looks like JSON
                    if text and (
                        text.strip().startswith("{") and text.strip().endswith("}")
                    ):
                        json_data = json.loads(text)
                except json.JSONDecodeError:
                    pass

            if hasattr(candidate, "finish_reason"):
                finish_reason = candidate.finish_reason.name
        return cls(text=text, json_data=json_data, finish_reason=finish_reason)


class StreamChunk:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_gemini_chunk(cls, chunk: Any):
        text = ""
        if chunk and hasattr(chunk, "candidates") and chunk.candidates:
            candidate = chunk.candidates[0]
            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                text_parts = [
                    part.text
                    for part in candidate.content.parts
                    if hasattr(part, "text")
                ]
                text = " ".join(text_parts)
        return cls(text=text)


class EmbeddingResponse:
    def __init__(
        self,
        embedding: Optional[List[float]] = None,
        embeddings: Optional[List[List[float]]] = None,
    ):
        self.embedding = embedding
        self.embeddings = embeddings

    @classmethod
    def from_gemini_response(cls, response: Any):
        embedding = None
        embeddings = None
        if (
            response
            and hasattr(response, "embedding")
            and hasattr(response.embedding, "values")
        ):
            embedding = response.embedding.values
        elif response and hasattr(response, "embeddings") and response.embeddings:
            embeddings = [
                emb.values for emb in response.embeddings if hasattr(emb, "values")
            ]
        return cls(embedding=embedding, embeddings=embeddings)


class PerspectiveAPIRequest:
    def __init__(self, text: str):
        self.text = text


class PerspectiveAPIResponse:
    def __init__(self, scores: Dict[str, float]):
        self.scores = scores

    @classmethod
    def from_api_response(cls, response: Dict):
        scores = {}
        if "attributeScores" in response:
            for attr, data in response["attributeScores"].items():
                if "summaryScore" in data and "value" in data["summaryScore"]:
                    scores[attr] = data["summaryScore"]["value"]
        return cls(scores=scores)


class TranslateRequest:
    def __init__(
        self,
        text: Union[str, List[str]],
        target_language: str,
        source_language: Optional[str] = None,
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class TranslateResponse:
    def __init__(self, translated_text: Union[str, List[str]]):
        self.translated_text = translated_text

    @classmethod
    def from_api_response(cls, response: Any):
        if hasattr(response, "translations") and response.translations:
            if isinstance(response.translations, list):
                translated_text = [
                    t.translated_text
                    for t in response.translations
                    if hasattr(t, "translated_text")
                ]
                if len(translated_text) == 1:
                    return cls(translated_text=translated_text[0])
                return cls(translated_text=translated_text)
            elif hasattr(response.translations, "translated_text"):
                return cls(translated_text=response.translations.translated_text)
        return cls(translated_text="")


class SynthesizeSpeechRequest:
    def __init__(
        self,
        text: str,
        voice_name: str = "en-US-Standard-C",
        language_code: str = "en-US",
    ):
        self.text = text
        self.voice_name = voice_name
        self.language_code = language_code


class SynthesizeSpeechResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content
