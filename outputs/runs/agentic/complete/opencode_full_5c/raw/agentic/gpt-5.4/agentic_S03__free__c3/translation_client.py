import os
from typing import Dict, List, Optional

import requests

from translation_models import normalize_language_code


GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"
OPENAI_EMBEDDINGS_ENDPOINT = "https://api.openai.com/v1/embeddings"
OPENAI_RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
PERSPECTIVE_ANALYZE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def get_google_api_key() -> str:
    api_key = os.environ["GOOGLE_CLOUD_API_KEY"]
    return api_key


def get_openai_api_key() -> str:
    return os.environ["OPENAI_API_KEY"]


def get_perspective_api_key() -> str:
    return os.environ["PERSPECTIVE_API_KEY"]


def build_google_translate_params() -> Dict[str, str]:
    return {"key": get_google_api_key()}


def translate_with_google(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    fmt: str = "text",
    model: str = "nmt",
    preserve_formatting: bool = True,
) -> Dict:
    payload: Dict[str, object] = {
        "q": texts,
        "target": normalize_language_code(target_language),
        "format": fmt,
        "model": model,
    }
    normalized_source = normalize_language_code(source_language)
    if normalized_source:
        payload["source"] = normalized_source
    if preserve_formatting:
        payload["format"] = fmt
    response = requests.post(
        GOOGLE_TRANSLATE_ENDPOINT,
        params=build_google_translate_params(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def synthesize_google_speech(
    text: str, language_code: str, voice_name: Optional[str] = None
) -> Dict:
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": normalize_language_code(language_code) or language_code,
            "name": voice_name or "en-US-Chirp3-HD-Achernar",
        },
        "audioConfig": {"audioEncoding": "MP3"},
    }
    response = requests.post(
        GOOGLE_TTS_ENDPOINT,
        params=build_google_translate_params(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def create_openai_embedding(
    texts: List[str], model: str = "text-embedding-3-small"
) -> Dict:
    response = requests.post(
        OPENAI_EMBEDDINGS_ENDPOINT,
        headers={
            "Authorization": f"Bearer {get_openai_api_key()}",
            "Content-Type": "application/json",
        },
        json={"input": texts, "model": model},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def create_openai_response(prompt: str, model: str = "gpt-4.1-mini") -> Dict:
    response = requests.post(
        OPENAI_RESPONSES_ENDPOINT,
        headers={
            "Authorization": f"Bearer {get_openai_api_key()}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def analyze_text_with_perspective(
    text: str, languages: Optional[List[str]] = None
) -> Dict:
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
    }
    if languages:
        payload["languages"] = [
            normalize_language_code(language) or language for language in languages
        ]
    response = requests.post(
        PERSPECTIVE_ANALYZE_ENDPOINT,
        params={"key": get_perspective_api_key()},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def extract_google_translations(payload: Dict) -> List[Dict]:
    return payload.get("data", {}).get("translations", [])
