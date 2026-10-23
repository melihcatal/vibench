from __future__ import annotations

import os
from typing import Tuple

import requests
from google.cloud import firestore
from supabase import Client, create_client


SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_ANON_KEY_ENV = "SUPABASE_ANON_KEY"
SUPABASE_SERVICE_ROLE_KEY_ENV = "SUPABASE_SERVICE_ROLE_KEY"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
GOOGLE_CLOUD_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"


class ConfigError(RuntimeError):
    pass


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def get_supabase_client(use_service_role: bool = False) -> Client:
    url = require_env(SUPABASE_URL_ENV)
    key_name = SUPABASE_SERVICE_ROLE_KEY_ENV if use_service_role else SUPABASE_ANON_KEY_ENV
    key = require_env(key_name)
    return create_client(url, key)


def get_supabase_auth_rest() -> Tuple[str, dict]:
    url = require_env(SUPABASE_URL_ENV).rstrip("/")
    anon_key = require_env(SUPABASE_ANON_KEY_ENV)
    headers = {
        "apikey": anon_key,
        "Content-Type": "application/json",
    }
    return f"{url}/auth/v1", headers


def get_deepl_headers() -> dict:
    return {
        "Authorization": f"DeepL-Auth-Key {require_env(DEEPL_API_KEY_ENV)}",
        "Content-Type": "application/json",
    }


def get_openai_headers() -> dict:
    return {
        "Authorization": f"Bearer {require_env(OPENAI_API_KEY_ENV)}",
        "Content-Type": "application/json",
    }


def get_firestore_client() -> firestore.Client:
    project = require_env(GOOGLE_CLOUD_PROJECT_ENV)
    return firestore.Client(project=project)


def post_json(url: str, headers: dict, payload: dict, timeout: int = 30) -> dict:
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()
