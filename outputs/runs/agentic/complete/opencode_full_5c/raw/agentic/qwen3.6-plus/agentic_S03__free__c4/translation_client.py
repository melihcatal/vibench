import os
from typing import Optional

import requests

from translation_models import (
    normalize_language_code,
    validate_language_code,
    parse_google_translate_response,
    build_google_translate_payload,
    build_google_tts_payload,
)

GOOGLE_TRANSLATE_API_BASE = "https://translation.googleapis.com"
GOOGLE_TTS_API_BASE = "https://texttospeech.googleapis.com"
GOOGLE_VERTEX_AI_BASE = "https://us-central1-aiplatform.googleapis.com"


def get_google_api_key() -> str:
    api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        api_key = os.environ.get("GOOGLE_CLOUD_API_KEY", "")
    return api_key


def get_google_credentials_path() -> Optional[str]:
    return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


def build_auth_headers(api_key: Optional[str] = None) -> dict[str, str]:
    key = api_key or get_google_api_key()
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if key:
        headers["X-Goog-Api-Key"] = key
    return headers


def translate_single_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    format_type: str = "text",
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> dict:
    if not validate_language_code(target_language):
        raise ValueError(f"Invalid target language code: {target_language}")
    if source_language and not validate_language_code(source_language):
        raise ValueError(f"Invalid source language code: {source_language}")

    payload = build_google_translate_payload(
        text=text,
        target_language=target_language,
        source_language=source_language,
        format_type=format_type,
        model=model,
    )

    headers = build_auth_headers(api_key)
    url = f"{GOOGLE_TRANSLATE_API_BASE}/language/translate/v2"

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def translate_batch_texts(
    texts: list[str],
    target_language: str,
    source_language: Optional[str] = None,
    format_type: str = "text",
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> list[dict]:
    if not texts:
        return []

    headers = build_auth_headers(api_key)
    url = f"{GOOGLE_TRANSLATE_API_BASE}/language/translate/v2"

    results = []
    for text in texts:
        payload = build_google_translate_payload(
            text=text,
            target_language=target_language,
            source_language=source_language,
            format_type=format_type,
            model=model,
        )
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        results.append(response.json())

    return results


def translate_with_html(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "nmt",
    api_key: Optional[str] = None,
) -> dict:
    return translate_single_text(
        text=text,
        target_language=target_language,
        source_language=source_language,
        format_type="html",
        model=model,
        api_key=api_key,
    )


def generate_audio_preview(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    api_key: Optional[str] = None,
) -> bytes:
    payload = build_google_tts_payload(
        text=text,
        language_code=language_code,
        voice_name=voice_name,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    headers = build_auth_headers(api_key)
    url = f"{GOOGLE_TTS_API_BASE}/v1/text:synthesize"

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()
    import base64

    return base64.b64decode(result.get("audioContent", ""))


def get_vertex_ai_embedding(
    text: str,
    project_id: Optional[str] = None,
    location: str = "us-central1",
    api_key: Optional[str] = None,
) -> list[float]:
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")

    endpoint = f"{GOOGLE_VERTEX_AI_BASE}/v1/projects/{project}/locations/{location}/publishers/google/models/textembedding-gecko@003:predict"

    payload = {
        "instances": [{"content": text}],
        "parameters": {"autoTruncate": True},
    }

    headers = build_auth_headers(api_key)
    response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()
    return result.get("predictions", [{}])[0].get("embeddings", {}).get("values", [])


def check_content_safety(
    text: str,
    api_key: Optional[str] = None,
) -> dict:
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    headers = build_auth_headers(api_key)
    response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
