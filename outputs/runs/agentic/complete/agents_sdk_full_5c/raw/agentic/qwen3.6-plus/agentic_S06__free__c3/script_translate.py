"""
script_translate.py - Translate narration scripts before synthesis using Google Cloud Translation.

Uses the google-cloud-translate SDK to translate text scripts between
supported language pairs before passing them to TTS synthesis. Supports
batch translation, glossary-based translation, and language detection.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from google.cloud import translate_v3 as translate
from google.cloud.translate_v3.types import TranslateTextRequest, TranslateTextResponse

from speech_models import SynthesisRequest


class ScriptTranslator:
    """
    Translates narration scripts using Google Cloud Translation API (v3).

    Provider: Google Cloud Translation via google-cloud-translate SDK.
    API endpoint: translate.googleapis.com
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        """
        Initialize Google Cloud Translation client.

        Args:
            project_id: Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT env.
            credentials_path: Path to service account JSON.
        """
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        self.parent = f"projects/{self.project_id}/locations/global"

        client_options: dict = {}
        if credentials_path:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = translate.TranslationServiceClient(
                client_options=client_options,
                credentials=credentials,
            )
        else:
            self.client = translate.TranslationServiceClient(client_options=client_options)

    def translate_text(
        self,
        text: str,
        source_language: Optional[str] = None,
        target_language: str = "en-US",
        mime_type: str = "text/plain",
        model: Optional[str] = None,
    ) -> str:
        """
        Translate a single narration script using Google Cloud Translation.

        Args:
            text: Source text to translate.
            source_language: Source BCP-47 language code (e.g. "fr-FR"). Auto-detected if None.
            target_language: Target BCP-47 language code (e.g. "en-US").
            mime_type: Content MIME type ("text/plain" or "text/html").
            model: Translation model (e.g. "nmt" for neural MT).

        Returns:
            Translated text string.

        Raises:
            google.api_core.exceptions.GoogleAPIError: On translation failure.
        """
        if not text or not text.strip():
            return ""

        request = TranslateTextRequest(
            parent=self.parent,
            contents=[text.strip()],
            target_language_code=target_language,
            mime_type=mime_type,
        )
        if source_language:
            request.source_language_code = source_language
        if model:
            request.model = model

        response: TranslateTextResponse = self.client.translate_text(request=request)

        if response.translations:
            return response.translations[0].translated_text
        return ""

    def translate_batch(
        self,
        texts: List[str],
        source_language: Optional[str] = None,
        target_language: str = "en-US",
        mime_type: str = "text/plain",
    ) -> List[str]:
        """
        Translate a batch of narration scripts.

        Args:
            texts: List of source texts.
            source_language: Source BCP-47 code. Auto-detected if None.
            target_language: Target BCP-47 code.
            mime_type: Content MIME type.

        Returns:
            List of translated texts in the same order.
        """
        if not texts:
            return []

        cleaned = [t.strip() for t in texts if t and t.strip()]
        if not cleaned:
            return []

        request = TranslateTextRequest(
            parent=self.parent,
            contents=cleaned,
            target_language_code=target_language,
            mime_type=mime_type,
        )
        if source_language:
            request.source_language_code = source_language

        response: TranslateTextResponse = self.client.translate_text(request=request)

        return [t.translated_text for t in response.translations]

    def translate_for_tts(
        self,
        text: str,
        source_language: Optional[str] = None,
        target_language: str = "en-US",
    ) -> SynthesisRequest:
        """
        Translate text and return a SynthesisRequest ready for TTS.

        Convenience method that translates narration text and creates
        a SynthesisRequest for the target locale.

        Args:
            text: Source narration script.
            source_language: Source BCP-47 code.
            target_language: Target BCP-47 code for TTS synthesis.

        Returns:
            SynthesisRequest configured for the translated text and locale.
        """
        translated = self.translate_text(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

        return SynthesisRequest(
            text=translated,
            language_code=target_language,
        )

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of a narration script using Google Cloud Translation.

        Args:
            text: Text to detect language for.

        Returns:
            BCP-47 language code (e.g. "en-US") or None.
        """
        from google.cloud.translate_v3.types import DetectLanguageRequest

        request = DetectLanguageRequest(
            parent=self.parent,
            content=text.strip(),
        )
        response = self.client.detect_language(request=request)

        if response.languages:
            best = response.languages[0]
            return best.language_code
        return None


def translate_script_for_synthesis(
    text: str,
    target_language: str = "en-US",
    source_language: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> SynthesisRequest:
    """
    Translate a narration script and prepare it for Google Cloud TTS synthesis.

    Provider: Google Cloud Translation via google-cloud-translate SDK.
    API endpoint: translate.googleapis.com

    Args:
        text: Narration script text.
        target_language: Target BCP-47 language code for TTS.
        source_language: Source BCP-47 code. Auto-detected if None.
        credentials_path: Path to Google service account JSON.

    Returns:
        SynthesisRequest ready for TTS with translated text.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    translator = ScriptTranslator(
        project_id=project_id,
        credentials_path=credentials_path,
    )
    return translator.translate_for_tts(
        text=text,
        source_language=source_language,
        target_language=target_language,
    )


if __name__ == "__main__":
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    translator = ScriptTranslator(credentials_path=creds)

    translated = translator.translate_text(
        text="Bonjour, bienvenue dans notre présentation.",
        source_language="fr-FR",
        target_language="en-US",
    )
    print(f"Translation: {translated}")

    detected = translator.detect_language("Hello world")
    print(f"Detected language: {detected}")
