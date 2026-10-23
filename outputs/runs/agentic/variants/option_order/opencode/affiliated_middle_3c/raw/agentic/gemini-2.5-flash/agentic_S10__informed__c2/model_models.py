import os
from typing import List, Dict, Any, Optional


class LLMRequest:
    text_content: str
    model_name: str = "gemini-pro"
    temperature: float = 0.7
    max_output_tokens: int = 1024

    def __init__(
        self,
        text_content: str,
        model_name: str = "gemini-pro",
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
    ):
        self.text_content = text_content
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens


class LLMContextRequest(LLMRequest):
    context: str
    question: str

    def __init__(
        self,
        question: str,
        context: str,
        model_name: str = "gemini-pro",
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
    ):
        super().__init__(
            text_content="",
            model_name=model_name,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        self.question = question
        self.context = context


class LLMResponse:
    output_text: str

    def __init__(self, output_text: str):
        self.output_text = output_text


class JSONExtractRequest(LLMRequest):
    json_schema: Dict[str, Any]

    def __init__(
        self,
        text_content: str,
        json_schema: Dict[str, Any],
        model_name: str = "gemini-pro",
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
    ):
        super().__init__(
            text_content=text_content,
            model_name=model_name,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        self.json_schema = json_schema


class JSONExtractResponse:
    extracted_json: Dict[str, Any]

    def __init__(self, extracted_json: Dict[str, Any]):
        self.extracted_json = extracted_json


class ContentSafetyRequest:
    text_content: str

    def __init__(self, text_content: str):
        self.text_content = text_content


class ContentSafetyResponse:
    is_safe: bool

    def __init__(self, is_safe: bool):
        self.is_safe = is_safe


class TranslateRequest:
    text_content: str
    target_language: str

    def __init__(self, text_content: str, target_language: str):
        self.text_content = text_content
        self.target_language = target_language


class TranslateResponse:
    translated_text: str

    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class EmbeddingRequest:
    text_content: str

    def __init__(self, text_content: str):
        self.text_content = text_content


class EmbeddingResponse:
    embedding: List[float]

    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class SpokenBriefRequest:
    text_content: str

    def __init__(self, text_content: str):
        self.text_content = text_content


class SpokenBriefResponse:
    audio_content: bytes

    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content
