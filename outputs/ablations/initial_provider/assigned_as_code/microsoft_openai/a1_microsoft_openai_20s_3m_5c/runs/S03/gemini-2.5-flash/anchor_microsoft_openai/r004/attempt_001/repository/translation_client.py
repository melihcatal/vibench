import os
import requests
from typing import List, Dict, Any
from translation_models import (
    TranslationRequest, BatchTranslationRequest, MarkupTranslationRequest,
    DictionaryTranslationRequest, TranslationResponse, BatchTranslationResponse,
    MarkupTranslationResponse, DictionaryTranslationResponse
)

class AzureTranslationClient:
    def __init__(self, api_key: str = None, region: str = None):
        self.api_key = api_key or os.environ.get("AZURE_TRANSLATOR_API_KEY")
        self.region = region or os.environ.get("AZURE_TRANSLATOR_REGION")
        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"

        if not self.api_key:
            raise ValueError("Azure Translator API key not provided or found in AZURE_TRANSLATOR_API_KEY environment variable.")
        if not self.region:
            raise ValueError("Azure Translator region not provided or found in AZURE_TRANSLATOR_REGION environment variable.")

    def _get_headers(self) -> Dict[str, str]:
        return {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        params = {
            'api-version': '3.0',
            'from': request.source_language,
            'to': request.target_language
        }
        body = [{'Text': request.text}]
        response = requests.post(self.endpoint, headers=self._get_headers(), params=params, json=body, timeout=30)
        response.raise_for_status()
        translated_text = response.json()[0]['translations'][0]['text']
        return TranslationResponse(text=translated_text, source_language=request.source_language, target_language=request.target_language)

    def batch_translate(self, request: BatchTranslationRequest) -> BatchTranslationResponse:
        params = {
            'api-version': '3.0',
            'from': request.source_language,
            'to': request.target_language
        }
        body = [{'Text': text} for text in request.texts]
        response = requests.post(self.endpoint, headers=self._get_headers(), params=params, json=body, timeout=30)
        response.raise_for_status()
        translated_texts = [res['translations'][0]['text'] for res in response.json()]
        return BatchTranslationResponse(texts=translated_texts, source_language=request.source_language, target_language=request.target_language)

    def translate_markup(self, request: MarkupTranslationRequest) -> MarkupTranslationResponse:
        params = {
            'api-version': '3.0',
            'from': request.source_language,
            'to': request.target_language,
            'textType': 'html'
        }
        body = [{'Text': request.html}]
        response = requests.post(self.endpoint, headers=self._get_headers(), params=params, json=body, timeout=30)
        response.raise_for_status()
        translated_html = response.json()[0]['translations'][0]['text']
        return MarkupTranslationResponse(html=translated_html, source_language=request.source_language, target_language=request.target_language)

    def translate_dictionary_values(self, request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
        translated_data = {}
        texts_to_translate = list(request.data.values())
        original_keys = list(request.data.keys())

        if not texts_to_translate:
            return DictionaryTranslationResponse(data={}, source_language=request.source_language, target_language=request.target_language)

        batch_request = BatchTranslationRequest(
            texts=texts_to_translate,
            source_language=request.source_language,
            target_language=request.target_language
        )
        batch_response = self.batch_translate(batch_request)

        for i, key in enumerate(original_keys):
            translated_data[key] = batch_response.texts[i]

        return DictionaryTranslationResponse(data=translated_data, source_language=request.source_language, target_language=request.target_language)
