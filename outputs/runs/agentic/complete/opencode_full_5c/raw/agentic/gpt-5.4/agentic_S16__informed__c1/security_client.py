from __future__ import annotations

import os
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


DEFAULT_AZURE_VAULT_URL_ENV = "AZURE_KEY_VAULT_URL"


def get_vault_url(explicit_url: Optional[str] = None) -> str:
    vault_url = explicit_url or os.getenv(DEFAULT_AZURE_VAULT_URL_ENV)
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL is required")
    return vault_url


def get_secret_client(vault_url: Optional[str] = None) -> SecretClient:
    return SecretClient(
        vault_url=get_vault_url(vault_url), credential=DefaultAzureCredential()
    )


def get_openai_client(api_key: Optional[str] = None):
    from openai import OpenAI

    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=resolved_api_key)


def get_perspective_headers(api_key: Optional[str] = None) -> dict:
    resolved_api_key = api_key or os.getenv("PERSPECTIVE_API_KEY")
    if not resolved_api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    return {"x-goog-api-key": resolved_api_key, "Content-Type": "application/json"}


def get_deepl_translator(auth_key: Optional[str] = None):
    import deepl

    resolved_auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not resolved_auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return deepl.Translator(resolved_auth_key)
