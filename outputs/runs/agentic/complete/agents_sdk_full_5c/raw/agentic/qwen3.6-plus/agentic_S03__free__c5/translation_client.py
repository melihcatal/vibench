"""
Local configuration and client helper utilities for General Text Translation.
Provides a Google Cloud Translation client wrapper with connection management.
"""
import os
import json
from typing import Optional, List, Dict, Any
from google.cloud import translate_v3 as translate
from google.api_core import retry
from google.oauth2 import service_account
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    build_translation_payload,
    parse_translation_response,
)

GOOGLE_CLOUD_TRANSLATION_ENDPOINT = "translate.googleapis.com"
GOOGLE_NMT_MODEL = "nmt"
GOOGLE_BASE_MODEL = "base"
GOOGLE_DEFAULT_MODEL = f"projects/{{project_id}}/locations/global/models/{GOOGLE_NMT_MODEL}"


class TranslationClient:
    """Google Cloud Translation API v3 client wrapper."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "global",
        credentials_path: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        self.location = location
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS", ""
        )
        self.default_model = default_model or GOOGLE_DEFAULT_MODEL.format(
            project_id=self.project_id
        )
        self._client = None

    @property
    def client(self) -> translate.TranslationServiceClient:
        """Lazy initialization of the Google Translate client."""
        if self._client is None:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = translate.TranslationServiceClient(
                    credentials=credentials
                )
            else:
                self._client = translate.TranslationServiceClient()
        return self._client

    @property
    def parent(self) -> str:
        """Return the Google Cloud parent resource path."""
        return f"projects/{self.project_id}/locations/{self.location}"

    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        mime_type: str = "text/plain",
        model: Optional[str] = None,
        retry_config: Optional[retry.Retry] = None,
    ) -> TranslationResponse:
        """Translate a single text string using Google Cloud Translation API v3."""
        payload = build_translation_payload(
            text=text,
            target_language=target_language,
            source_language=source_language,
            mime_type=mime_type,
            model=model or self.default_model,
        )

        request = translate.TranslateTextRequest(
            parent=self.parent,
            contents=payload["contents"],
            target_language_code=payload["target_language_code"],
            mime_type=payload.get("mime_type", "text/plain"),
        )

        if payload.get("source_language_code"):
            request.source_language_code = payload["source_language_code"]
        if payload.get("model"):
            request.model = payload["model"]

        response = self.client.translate_text(
            request=request,
            retry=retry_config or retry.Retry(
                initial=0.5, maximum=30.0, multiplier=2.0
            ),
        )

        return parse_translation_response(response)

    def batch_translate(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None,
        mime_type: str = "text/plain",
        model: Optional[str] = None,
    ) -> BatchTranslationResponse:
        """Translate a list of strings in a single request to Google Cloud Translation API."""
        target_lang = target_language
        source_lang = source_language if source_language else ""
        model_str = model or self.default_model

        request = translate.TranslateTextRequest(
            parent=self.parent,
            contents=texts,
            target_language_code=target_lang,
            mime_type=mime_type,
        )

        if source_lang:
            request.source_language_code = source_lang
        if model_str:
            request.model = model_str

        response = self.client.translate_text(request=request)

        translations = []
        total_chars = 0
        for i, translation in enumerate(response.translations):
            trans_resp = TranslationResponse(
                translated_text=translation.translated_text,
                source_language=response.source_language_code or "auto",
                target_language=translation.detected_language_code or target_lang,
                confidence=getattr(
                    translation, "detected_language_confidence", 1.0
                ),
                model_used=model_str,
                character_count=len(translation.translated_text),
            )
            translations.append(trans_resp)
            total_chars += trans_resp.character_count

        return BatchTranslationResponse(
            translations=translations, total_characters=total_chars
        )

    def translate_html(
        self,
        html_content: str,
        target_language: str,
        source_language: Optional[str] = None,
        model: Optional[str] = None,
    ) -> TranslationResponse:
        """Translate HTML content preserving markup using Google Cloud Translation API."""
        return self.translate_text(
            text=html_content,
            target_language=target_language,
            source_language=source_language,
            mime_type="text/html",
            model=model,
        )


def create_default_client() -> TranslationClient:
    """Create a TranslationClient from environment configuration."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    location = os.environ.get("GOOGLE_TRANSLATION_LOCATION", "global")
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

    return TranslationClient(
        project_id=project_id,
        location=location,
        credentials_path=credentials_path if credentials_path else None,
    )
