"""
Translate onboarding copy into the user's locale using Google Cloud Translation API.

Uses Google Cloud Translation service (google-cloud-translate SDK).
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model: google-cloud-translate v3 (general/nmt)
"""

import os
from typing import Optional, Dict, List

from google.cloud import translate_v2 as translate


# Default onboarding welcome messages keyed by message identifier
DEFAULT_ONBOARDING_COPY: Dict[str, str] = {
    "welcome_title": "Welcome to Our Platform",
    "welcome_body": (
        "Thank you for creating an account. We're excited to have you on board. "
        "Please complete your profile to get started with your personalized experience."
    ),
    "action_required": "Complete your profile setup",
    "help_text": "If you need assistance, our support team is available 24/7.",
    "next_steps": (
        "Your next steps: verify your email address, upload a profile photo, "
        "and explore the dashboard."
    ),
}


class WelcomeTranslator:
    """Handles translation of onboarding welcome copy using Google Cloud Translation."""

    def __init__(self, target_language: Optional[str] = None):
        """
        Initialize the translator.

        Args:
            target_language: ISO 639-1 language code (e.g., 'es', 'fr', 'ja').
        """
        self.client = translate.Client()
        self.target_language = target_language

    def translate_text(self, text: str, target_lang: Optional[str] = None) -> str:
        """
        Translate a single string into the target language.

        Uses Google Cloud Translation API v2 with the nmt (neural machine
        translation) model.
        """
        lang = target_lang or self.target_language
        if not lang:
            return text

        result = self.client.translate(
            text,
            target_language=lang,
            format_="text",
        )
        return result["translatedText"]

    def translate_onboarding_copy(
        self,
        target_lang: Optional[str] = None,
        custom_copy: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Translate the full onboarding copy bundle into the target locale.

        Args:
            target_lang: ISO 639-1 language code.
            custom_copy: Optional override copy to translate instead of defaults.

        Returns:
            Dict mapping message identifiers to translated strings.
        """
        lang = target_lang or self.target_language
        if not lang:
            return custom_copy or DEFAULT_ONBOARDING_COPY

        source = custom_copy if custom_copy is not None else DEFAULT_ONBOARDING_COPY
        translated: Dict[str, str] = {}

        for key, value in source.items():
            translated[key] = self.translate_text(value, lang)

        return translated

    def translate_batch(
        self,
        texts: List[str],
        target_lang: Optional[str] = None,
    ) -> List[str]:
        """
        Translate a batch of strings in a single API call to Google Cloud Translation.
        """
        lang = target_lang or self.target_language
        if not lang:
            return texts

        results = self.client.translate(
            texts,
            target_language=lang,
            format_="text",
        )
        return [r["translatedText"] for r in results]


def translate_welcome_copy(
    user_locale: str,
    custom_copy: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Convenience function to translate onboarding copy for a given user locale.

    Uses Google Cloud Translation service.
    """
    translator = WelcomeTranslator(target_language=user_locale)
    return translator.translate_onboarding_copy(
        target_lang=user_locale,
        custom_copy=custom_copy,
    )
