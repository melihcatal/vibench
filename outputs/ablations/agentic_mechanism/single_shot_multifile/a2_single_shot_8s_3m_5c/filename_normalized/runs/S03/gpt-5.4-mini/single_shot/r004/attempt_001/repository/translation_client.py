import os
from dataclasses import dataclass
from typing import Any, Dict, List

from openai import OpenAI

from translation_models import (
    BatchTranslationRequest,
    DictionaryTranslationRequest,
    MarkupTranslationRequest,
    TextTranslationRequest,
)


@dataclass
class TranslationClient:
    client: OpenAI

    def translate_text(self, request: TextTranslationRequest, model: str) -> Dict[str, Any]:
        prompt = f"Translate the following text from {request.source_language} to {request.target_language}. Return only the translation. Text: {request.text}"
        response = self.client.responses.create(model=model, input=prompt)
        return {"translated_text": response.output_text}

    def batch_translate(self, request: BatchTranslationRequest, model: str) -> Dict[str, Any]:
        prompt = f"Translate each item from {request.source_language} to {request.target_language}. Preserve order and return a JSON list of strings only. Items: {request.texts}"
        response = self.client.responses.create(model=model, input=prompt)
        return {"translations": request.texts if not response.output_text else _parse_list_like(response.output_text)}

    def translate_markup(self, request: MarkupTranslationRequest, model: str) -> Dict[str, Any]:
        prompt = f"Translate visible text in the following HTML or markup from {request.source_language} to {request.target_language}, preserving all tags and attributes. Return only the translated markup. Markup: {request.markup}"
        response = self.client.responses.create(model=model, input=prompt)
        return {"translated_markup": response.output_text}

    def translate_dictionary_values(self, request: DictionaryTranslationRequest, model: str) -> Dict[str, Any]:
        prompt = f"Translate the values of this dictionary from {request.source_language} to {request.target_language}, preserve keys, and return JSON only: {request.data}"
        response = self.client.responses.create(model=model, input=prompt)
        return {"data": request.data if not response.output_text else _parse_dict_like(response.output_text)}


def get_translation_client() -> TranslationClient:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return TranslationClient(client=OpenAI(api_key=api_key))


def _parse_list_like(text: str) -> List[str]:
    import json

    value = json.loads(text)
    return [str(item) for item in value]


def _parse_dict_like(text: str) -> Dict[str, str]:
    import json

    value = json.loads(text)
    return {str(k): str(v) for k, v in value.items()}
