import os
from dataclasses import dataclass

from openai import OpenAI
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


@dataclass
class TranslationConfig:
    provider: str = os.getenv("TRANSLATION_PROVIDER", "openai")
    openai_model: str = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    azure_endpoint: str | None = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    azure_key: str | None = os.getenv("AZURE_TRANSLATOR_KEY")
    azure_region: str | None = os.getenv("AZURE_TRANSLATOR_REGION")


def get_config() -> TranslationConfig:
    return TranslationConfig()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_azure_translation_client() -> TextTranslationClient:
    endpoint = os.environ["AZURE_TRANSLATOR_ENDPOINT"]
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    return TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def normalize_language(language: str) -> str:
    return language.strip().lower()
