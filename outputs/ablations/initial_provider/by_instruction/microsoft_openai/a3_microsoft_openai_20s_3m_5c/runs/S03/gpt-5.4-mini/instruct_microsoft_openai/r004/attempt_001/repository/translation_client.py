import os
from functools import lru_cache

from openai import OpenAI

AZURE_OPENAI_ENDPOINT_ENV = "AZURE_OPENAI_ENDPOINT"
AZURE_OPENAI_API_KEY_ENV = "AZURE_OPENAI_API_KEY"
AZURE_OPENAI_DEPLOYMENT_ENV = "AZURE_OPENAI_DEPLOYMENT"
AZURE_OPENAI_API_VERSION = "2024-10-21"


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ[AZURE_OPENAI_API_KEY_ENV], base_url=f"{os.environ[AZURE_OPENAI_ENDPOINT_ENV].rstrip('/')}/openai/deployments/{os.environ[AZURE_OPENAI_DEPLOYMENT_ENV]}")


def get_translation_deployment() -> str:
    return os.environ[AZURE_OPENAI_DEPLOYMENT_ENV]


def build_translation_messages(text: str, source_language: str | None, target_language: str) -> list[dict[str, str]]:
    system = "You are a translation engine that returns only the translated text."
    user = f"Translate from {source_language or 'auto-detected'} to {target_language}: {text}"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]
