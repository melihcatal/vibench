"""
Local helper: safety_client.py
Provides configuration loading, client initialization, and shared utilities
for text content safety provider integrations.
"""

import os
from typing import Optional, Dict, Any


SAFETY_CONFIG_KEYS = {
    "OPENAI_API_KEY": None,
    "GOOGLE_PERSPECTIVE_API_KEY": None,
    "AWS_REGION": "us-east-1",
    "DEEPL_API_KEY": None,
    "ELEVENLABS_API_KEY": None,
    "DEFAULT_MODERATION_MODEL": "text-moderation-latest",
    "DEFAULT_SUMMARY_MODEL": "gpt-4o",
    "DEFAULT_EMBEDDING_MODEL": "text-embedding-3-small",
    "DEFAULT_VOICE_ID": "21m00Tcm4TlvDq8ikWAM",
}


def load_safety_config(override_env: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Load safety integration configuration from environment variables."""
    config = {}
    for key, default in SAFETY_CONFIG_KEYS.items():
        value = os.environ.get(key)
        if value is None:
            value = default
        config[key] = value
    if override_env:
        config.update(override_env)
    return config


def get_openai_client(config: Optional[Dict[str, Any]] = None):
    """Return an initialized OpenAI client for moderation and embeddings."""
    from openai import OpenAI
    if config is None:
        config = load_safety_config()
    api_key = config.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set for OpenAI safety integrations")
    return OpenAI(api_key=api_key)


def get_perspective_api_key(config: Optional[Dict[str, Any]] = None) -> str:
    """Return the Google Perspective / Comment Analyzer API key."""
    if config is None:
        config = load_safety_config()
    key = config.get("GOOGLE_PERSPECTIVE_API_KEY") or os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_PERSPECTIVE_API_KEY must be set for Perspective API integrations")
    return key


def get_deepl_api_key(config: Optional[Dict[str, Any]] = None) -> str:
    """Return the DeepL API key for translation."""
    if config is None:
        config = load_safety_config()
    key = config.get("DEEPL_API_KEY") or os.environ.get("DEEPL_API_KEY")
    if not key:
        raise ValueError("DEEPL_API_KEY must be set for DeepL translation integrations")
    return key


def get_elevenlabs_api_key(config: Optional[Dict[str, Any]] = None) -> str:
    """Return the ElevenLabs API key for TTS."""
    if config is None:
        config = load_safety_config()
    key = config.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY must be set for ElevenLabs TTS integrations")
    return key


def chunk_texts(texts: list[str], max_chunk_size: int = 20) -> list[list[str]]:
    """Split a list of texts into chunks for batch API calls."""
    chunks = []
    for i in range(0, len(texts), max_chunk_size):
        chunks.append(texts[i : i + max_chunk_size])
    return chunks
