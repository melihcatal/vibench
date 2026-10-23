from __future__ import annotations

import os

import deepl


def get_deepl_auth_key() -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    return auth_key


def get_deepl_client() -> deepl.Translator:
    return deepl.Translator(get_deepl_auth_key())


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def get_perspective_api_key() -> str:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY is required")
    return api_key


def get_elevenlabs_api_key() -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    return api_key
