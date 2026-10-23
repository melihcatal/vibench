import os
from dataclasses import dataclass
from typing import Iterable

from google.cloud import translate_v2 as translate


DEFAULT_PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"
DEFAULT_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


@dataclass(frozen=True)
class TranslationClientConfig:
    project_id: str | None = None
    credentials_path: str | None = None
    location: str = "global"

    @classmethod
    def from_env(cls) -> "TranslationClientConfig":
        return cls(
            project_id=os.environ.get(DEFAULT_PROJECT_ID_ENV),
            credentials_path=os.environ.get(DEFAULT_CREDENTIALS_ENV),
            location=os.environ.get("GOOGLE_CLOUD_TRANSLATION_LOCATION", "global"),
        )


def create_translation_client(config: TranslationClientConfig | None = None) -> translate.Client:
    if config is None:
        config = TranslationClientConfig.from_env()
    if config.credentials_path and not os.environ.get(DEFAULT_CREDENTIALS_ENV):
        os.environ[DEFAULT_CREDENTIALS_ENV] = config.credentials_path
    if config.project_id and not os.environ.get(DEFAULT_PROJECT_ID_ENV):
        os.environ[DEFAULT_PROJECT_ID_ENV] = config.project_id
    return translate.Client(project=config.project_id)


def translate_text(text: str, target_language: str, source_language: str | None = None, config: TranslationClientConfig | None = None) -> str:
    client = create_translation_client(config)
    result = client.translate(text, target_language=target_language, source_language=source_language)
    return result["translatedText"]


def translate_texts(texts: Iterable[str], target_language: str, source_language: str | None = None, config: TranslationClientConfig | None = None) -> list[str]:
    client = create_translation_client(config)
    items = list(texts)
    if not items:
        return []
    results = client.translate(items, target_language=target_language, source_language=source_language)
    if isinstance(results, dict):
        results = [results]
    return [result["translatedText"] for result in results]
