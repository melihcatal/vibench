import os
import json
import requests
from typing import Optional, Dict, Any, List
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    MarkupTranslationRequest,
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
    normalize_language_code,
    normalize_text,
    build_translation_payload,
    parse_translation_response,
    parse_batch_translation_response,
)

GOOGLE_TRANSLATE_API_KEY = os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
GOOGLE_TRANSLATE_API_ENDPOINT = (
    "https://translation.googleapis.com/language/translate/v2"
)
GOOGLE_TTS_API_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"
GOOGLE_EMBEDDING_API_ENDPOINT = "https://us-central1-aiplatform.googleapis.com/v1"
GOOGLE_CONTENT_SAFETY_ENDPOINT = "https://language.googleapis.com/v1"
DEFAULT_GOOGLE_MODEL = "google-nmt"
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")


class GoogleTranslationClient:
    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        self.api_key = api_key or GOOGLE_TRANSLATE_API_KEY
        self.project_id = project_id or GOOGLE_PROJECT_ID
        self.base_url = GOOGLE_TRANSLATE_API_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
            }
        )

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        payload = build_translation_payload(request)
        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return parse_translation_response(response.json(), request)

    def batch_translate(
        self, request: BatchTranslationRequest
    ) -> BatchTranslationResponse:
        texts = [{"q": text} for text in request.texts]
        payload = {
            "q": request.texts,
            "source": normalize_language_code(request.source_language)
            if request.source_language
            else "",
            "target": normalize_language_code(request.target_language),
            "format": request.content_type,
            "model": request.model,
        }
        payload = {k: v for k, v in payload.items() if v}
        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return parse_batch_translation_response(response.json(), request)

    def translate_html(self, request: MarkupTranslationRequest) -> TranslationResponse:
        translation_req = TranslationRequest(
            text=request.markup_text,
            source_language=request.source_language,
            target_language=request.target_language,
            model=request.model,
            content_type="html",
        )
        return self.translate(translation_req)

    def translate_dictionary(
        self, request: DictionaryTranslationRequest
    ) -> DictionaryTranslationResponse:
        values = list(request.data.values())
        keys = list(request.data.keys())
        batch_req = BatchTranslationRequest(
            texts=values,
            source_language=request.source_language,
            target_language=request.target_language,
            model=request.model,
        )
        batch_response = self.batch_translate(batch_req)
        translated_data = {}
        for i, key in enumerate(keys):
            if i < len(batch_response.translations):
                translated_data[key] = batch_response.translations[i].translated_text
        return DictionaryTranslationResponse(
            translated_data=translated_data,
            original_keys=keys,
            target_language=request.target_language,
        )


class GoogleTextToSpeechClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GOOGLE_TRANSLATE_API_KEY
        self.base_url = GOOGLE_TTS_API_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
            }
        )

    def synthesize(
        self,
        text: str,
        language_code: str,
        voice_name: Optional[str] = None,
        encoding: str = "MP3",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
    ) -> Dict[str, Any]:
        if voice_name is None:
            voice_name = self._get_default_voice(language_code)
        payload = {
            "input": {"text": text},
            "voice": {
                "languageCode": normalize_language_code(language_code),
                "name": voice_name,
            },
            "audioConfig": {
                "audioEncoding": encoding,
                "speakingRate": speaking_rate,
                "pitch": pitch,
            },
        }
        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()

    def _get_default_voice(self, language_code: str) -> str:
        lang = normalize_language_code(language_code)
        voice_map = {
            "en-US": "en-US-Wavenet-D",
            "en-GB": "en-GB-Wavenet-A",
            "es-ES": "es-ES-Wavenet-B",
            "fr-FR": "fr-FR-Wavenet-A",
            "de-DE": "de-DE-Wavenet-A",
            "ja-JP": "ja-JP-Wavenet-A",
            "zh-CN": "cmn-CN-Wavenet-A",
            "ko-KR": "ko-KR-Wavenet-A",
            "pt-BR": "pt-BR-Wavenet-A",
            "it-IT": "it-IT-Wavenet-A",
            "ru-RU": "ru-RU-Wavenet-A",
            "ar-XA": "ar-XA-Wavenet-A",
            "hi-IN": "hi-IN-Wavenet-A",
        }
        return voice_map.get(lang, "en-US-Wavenet-D")


class GoogleEmbeddingClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        location: str = "us-central1",
    ):
        self.api_key = api_key or GOOGLE_TRANSLATE_API_KEY
        self.project_id = project_id or GOOGLE_PROJECT_ID
        self.location = location
        self.base_url = GOOGLE_EMBEDDING_API_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
            }
        )

    def embed_text(
        self, text: str, model: str = "textembedding-gecko@003"
    ) -> List[float]:
        endpoint = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{model}:predict"
        payload = {
            "instances": [{"content": text}],
            "parameters": {"autoTruncate": True},
        }
        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["predictions"][0]["embeddings"]["values"]

    def embed_texts(
        self, texts: List[str], model: str = "textembedding-gecko@003"
    ) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_text(text, model))
        return embeddings


class GoogleContentSafetyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GOOGLE_TRANSLATE_API_KEY
        self.base_url = GOOGLE_CONTENT_SAFETY_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
            }
        )

    def analyze_text(self, text: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/documents:analyzeEntities"
        payload = {
            "document": {
                "type": "PLAIN_TEXT",
                "content": text,
            },
            "encodingType": "UTF8",
        }
        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/documents:analyzeSentiment"
        payload = {
            "document": {
                "type": "PLAIN_TEXT",
                "content": text,
            },
            "encodingType": "UTF8",
        }
        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()


def load_config_from_env() -> Dict[str, str]:
    return {
        "api_key": GOOGLE_TRANSLATE_API_KEY,
        "project_id": GOOGLE_PROJECT_ID,
        "credentials_path": GOOGLE_APPLICATION_CREDENTIALS,
        "translate_endpoint": GOOGLE_TRANSLATE_API_ENDPOINT,
        "tts_endpoint": GOOGLE_TTS_API_ENDPOINT,
        "embedding_endpoint": GOOGLE_EMBEDDING_API_ENDPOINT,
        "default_model": DEFAULT_GOOGLE_MODEL,
    }


def create_translation_client(api_key: Optional[str] = None) -> GoogleTranslationClient:
    return GoogleTranslationClient(api_key=api_key)


def create_tts_client(api_key: Optional[str] = None) -> GoogleTextToSpeechClient:
    return GoogleTextToSpeechClient(api_key=api_key)


def create_embedding_client(
    api_key: Optional[str] = None, project_id: Optional[str] = None
) -> GoogleEmbeddingClient:
    return GoogleEmbeddingClient(api_key=api_key, project_id=project_id)


def create_safety_client(api_key: Optional[str] = None) -> GoogleContentSafetyClient:
    return GoogleContentSafetyClient(api_key=api_key)
