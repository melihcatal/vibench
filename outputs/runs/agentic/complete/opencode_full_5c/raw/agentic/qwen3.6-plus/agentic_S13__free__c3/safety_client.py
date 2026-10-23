from __future__ import annotations

import os
from typing import Any

import httpx


OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_BASE = "https://api.openai.com/v1"
PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com/v1alpha1"
AZURE_CONTENT_SAFETY_BASE = "https://{endpoint}.cognitiveservices.azure.com"
DEEPL_API_BASE = "https://api-free.deepl.com/v2"
ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"


def load_openai_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return key


def load_perspective_api_key() -> str:
    key = os.environ.get("GOOGLE_API_KEY", "")
    if not key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    return key


def load_azure_content_safety_config() -> dict[str, str]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )
    return {"endpoint": endpoint, "key": key}


def load_deepl_api_key() -> str:
    key = os.environ.get("DEEPL_API_KEY", "")
    if not key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    return key


def load_elevenlabs_api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    return key


def build_openai_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def build_azure_headers(subscription_key: str) -> dict[str, str]:
    return {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json",
    }


def build_deepl_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/json",
    }


def build_elevenlabs_headers(api_key: str) -> dict[str, str]:
    return {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }


async def call_openai_moderation(
    text: str, api_key: str | None = None, model: str = OPENAI_MODERATION_MODEL
) -> dict[str, Any]:
    if api_key is None:
        api_key = load_openai_api_key()
    headers = build_openai_headers(api_key)
    payload = {"input": text, "model": model}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{OPENAI_API_BASE}/moderations",
            headers=headers,
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()


async def call_openai_moderation_batch(
    texts: list[str], api_key: str | None = None, model: str = OPENAI_MODERATION_MODEL
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for text in texts:
        result = await call_openai_moderation(text, api_key=api_key, model=model)
        results.append(result)
    return results


async def call_openai_embeddings(
    text: str, api_key: str | None = None, model: str = OPENAI_EMBEDDING_MODEL
) -> dict[str, Any]:
    if api_key is None:
        api_key = load_openai_api_key()
    headers = build_openai_headers(api_key)
    payload = {"input": text, "model": model}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{OPENAI_API_BASE}/embeddings",
            headers=headers,
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()


async def call_openai_chat(
    messages: list[dict[str, str]],
    api_key: str | None = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
) -> dict[str, Any]:
    if api_key is None:
        api_key = load_openai_api_key()
    headers = build_openai_headers(api_key)
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json()


async def call_perspective_api(
    text: str,
    api_key: str | None = None,
    attributes: list[str] | None = None,
    languages: list[str] | None = None,
) -> dict[str, Any]:
    if api_key is None:
        api_key = load_perspective_api_key()
    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]
    if languages is None:
        languages = ["en"]
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PERSPECTIVE_API_BASE}/comments:analyze",
            params={"key": api_key},
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()


async def call_azure_content_safety(
    text: str,
    endpoint: str | None = None,
    key: str | None = None,
    api_version: str = "2024-09-01",
) -> dict[str, Any]:
    if endpoint is None or key is None:
        config = load_azure_content_safety_config()
        endpoint = config["endpoint"]
        key = config["key"]
    base_url = AZURE_CONTENT_SAFETY_BASE.format(endpoint=endpoint)
    headers = build_azure_headers(key)
    payload = {"text": text}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{base_url}/contentsafety/text:analyze",
            headers=headers,
            json=payload,
            params={"api-version": api_version},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()


async def call_deepl_translate(
    text: str,
    target_lang: str,
    api_key: str | None = None,
    source_lang: str | None = None,
) -> dict[str, Any]:
    if api_key is None:
        api_key = load_deepl_api_key()
    headers = build_deepl_headers(api_key)
    payload: dict[str, str] = {
        "text": text,
        "target_lang": target_lang,
    }
    if source_lang:
        payload["source_lang"] = source_lang
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{DEEPL_API_BASE}/translate",
            headers=headers,
            data=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()


async def call_elevenlabs_tts(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    api_key: str | None = None,
    model: str = "eleven_monolingual_v1",
    output_format: str = "mp3_44100_128",
) -> bytes:
    if api_key is None:
        api_key = load_elevenlabs_api_key()
    headers = build_elevenlabs_headers(api_key)
    payload = {
        "text": text,
        "model_id": model,
        "output_format": output_format,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}",
            headers=headers,
            json=payload,
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.content
