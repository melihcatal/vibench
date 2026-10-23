from __future__ import annotations

import os
from functools import lru_cache

from anthropic import Anthropic
from azure.ai.openai import OpenAIClient as AzureOpenAIClient
from google import genai
from openai import OpenAI
from azure.core.credentials import AzureKeyCredential


@lru_cache(maxsize=1)
def get_anthropic_client() -> Anthropic:
    return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@lru_cache(maxsize=1)
def get_azure_openai_client() -> AzureOpenAIClient:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    credential = AzureKeyCredential(os.environ["AZURE_OPENAI_API_KEY"])
    return AzureOpenAIClient(endpoint=endpoint, credential=credential)


@lru_cache(maxsize=1)
def get_gemini_client():
    return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def safety_model_name(task: str) -> str:
    mapping = {
        "moderation": os.environ.get("ANTHROPIC_SAFETY_MODEL", "claude-3-5-sonnet-20241022"),
        "batch_moderation": os.environ.get("OPENAI_SAFETY_MODEL", "gpt-4.1-mini"),
        "redaction": os.environ.get("AZURE_OPENAI_SAFETY_MODEL", "gpt-4o-mini"),
        "threshold": os.environ.get("GEMINI_SAFETY_MODEL", "gemini-2.0-flash"),
        "summary": os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
        "translation": os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        "embedding": os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
        "audio": os.environ.get("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts"),
    }
    return mapping[task]
