import os
import openai
from typing import List, Dict, Any
from translation_models import (
    TranslationRequest, TranslationResponse,
    BatchTranslationRequest, BatchTranslationResponse,
    MarkupTranslationRequest, TranslationResponse,
    DictionaryTranslationRequest, DictionaryTranslationResponse
)

class OpenAITranslationClient:
    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4") # Default to gpt-4 or user-defined

    def _call_openai_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        messages = [
            {"role": "system", "content": "You are a helpful translation assistant."},
            {"role": "user", "content": f"Translate the following text from {request.source_language or 'auto-detect'} to {request.target_language}:\n\n{request.text}"}
        ]
        translated_text = self._call_openai_chat_completion(messages)
        return TranslationResponse(
            translated_text=translated_text,
            source_language=request.source_language, # OpenAI might not return source lang easily, so propagate if provided
            target_language=request.target_language
        )

    def batch_translate_texts(self, request: BatchTranslationRequest) -> BatchTranslationResponse:
        translated_texts = []
        for text in request.texts:
            messages = [
                {"role": "system", "content": "You are a helpful translation assistant."},
                {"role": "user", "content": f"Translate the following text from {request.source_language or 'auto-detect'} to {request.target_language}:\n\n{text}"}
            ]
            translated_text = self._call_openai_chat_completion(messages)
            translated_texts.append(translated_text)
        return BatchTranslationResponse(
            translated_texts=translated_texts,
            source_language=request.source_language,
            target_language=request.target_language
        )

    def translate_markup(self, request: MarkupTranslationRequest) -> TranslationResponse:
        messages = [
            {"role": "system", "content": "You are a helpful translation assistant. Translate the provided markup, preserving all tags and structure. Only translate the translatable text content."},
            {"role": "user", "content": f"Translate the following {request.markup_type} content from {request.source_language or 'auto-detect'} to {request.target_language}. Preserve all markup tags and structure, only translating the text content inside:\n\n{request.markup_text}"}
        ]
        translated_markup = self._call_openai_chat_completion(messages)
        return TranslationResponse(
            translated_text=translated_markup,
            source_language=request.source_language,
            target_language=request.target_language
        )

    def translate_dictionary_values(self, request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
        translated_dict = {}
        for key, value in request.dictionary.items():
            messages = [
                {"role": "system", "content": "You are a helpful translation assistant."},
                {"role": "user", "content": f"Translate the following text from {request.source_language or 'auto-detect'} to {request.target_language}. This is a dictionary value, so only translate the value, not the key.\n\nText to translate: {value}"}
            ]
            translated_value = self._call_openai_chat_completion(messages)
            translated_dict[key] = translated_value
        return DictionaryTranslationResponse(
            translated_dictionary=translated_dict,
            source_language=request.source_language,
            target_language=request.target_language
        )
