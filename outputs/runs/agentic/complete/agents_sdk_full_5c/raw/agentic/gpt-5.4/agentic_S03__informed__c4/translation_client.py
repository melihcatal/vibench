from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v3 as translate

from translation_models import normalize_language_code


DEFAULT_TRANSLATION_MODEL = "general/nmt"
DEFAULT_LOCATION = os.getenv("GOOGLE_CLOUD_TRANSLATION_LOCATION", "global")


class GoogleTranslationClientFactory:
    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.location = location or DEFAULT_LOCATION
        self.model = model or DEFAULT_TRANSLATION_MODEL
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCLOUD_PROJECT must be set")

    def build(self) -> translate.TranslationServiceClient:
        return translate.TranslationServiceClient()

    def parent(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}"

    def model_path(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/models/{self.model}"


def build_translation_client(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    model: Optional[str] = None,
) -> tuple[translate.TranslationServiceClient, str, str]:
    factory = GoogleTranslationClientFactory(project_id=project_id, location=location, model=model)
    return factory.build(), factory.parent(), factory.model_path()


def normalize_translation_languages(source_language: Optional[str], target_language: str) -> tuple[Optional[str], str]:
    normalized_source = normalize_language_code(source_language)
    normalized_target = normalize_language_code(target_language)
    if not normalized_target:
        raise ValueError("target_language is required")
    return normalized_source, normalized_target
