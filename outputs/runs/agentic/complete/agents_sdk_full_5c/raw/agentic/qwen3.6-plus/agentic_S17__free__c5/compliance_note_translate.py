"""
compliance_note_translate.py - Translate encryption or compliance notes for reviewers using DeepL API.

Provider: DeepL Translation API
Service endpoint: api.deepl.com
Concrete model: DeepL Neural Machine Translation engine
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import requests

from security_models import ComplianceNote


SUPPORTED_DEEPL_LANGUAGES = {
    "EN": "English",
    "DE": "German",
    "FR": "French",
    "ES": "Spanish",
    "IT": "Italian",
    "PT": "Portuguese",
    "NL": "Dutch",
    "PL": "Polish",
    "RU": "Russian",
    "JA": "Japanese",
    "ZH": "Chinese",
    "KO": "Korean",
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "EL": "Greek",
    "FI": "Finnish",
    "HU": "Hungarian",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "RO": "Romanian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "UK": "Ukrainian",
    "NB": "Norwegian",
    "ID": "Indonesian",
    "TR": "Turkish",
}


DEEPL_API_BASE = "https://api.deepl.com/v2"
DEEPL_FREE_API_BASE = "https://api-free.deepl.com/v2"


class DeepLClient:
    """Client for DeepL Translation API (api.deepl.com)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        use_free_api: bool = False,
    ):
        self.api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
        self.base_url = DEEPL_FREE_API_BASE if use_free_api else DEEPL_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"DeepL-Auth-Key {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
    ) -> str:
        """
        Translate a single text using DeepL Neural Machine Translation.

        Uses the DeepL API at api.deepl.com to translate text between
        supported language pairs using their neural translation engine.

        Args:
            text: Text to translate.
            target_lang: Target language code (e.g., "DE", "FR", "ES").
            source_lang: Optional source language code. If None, DeepL auto-detects.
            formality: "more" or "less" for languages that support formality levels.

        Returns:
            Translated text string.
        """
        if target_lang not in SUPPORTED_DEEPL_LANGUAGES:
            raise ValueError(f"Unsupported target language: {target_lang}")

        payload: Dict[str, str] = {
            "text": text,
            "target_lang": target_lang.upper(),
        }

        if source_lang:
            if source_lang not in SUPPORTED_DEEPL_LANGUAGES:
                raise ValueError(f"Unsupported source language: {source_lang}")
            payload["source_lang"] = source_lang.upper()

        if formality:
            payload["formality"] = formality

        response = self.session.post(
            f"{self.base_url}/translate",
            data=payload,
        )

        response.raise_for_status()
        result = response.json()

        if not result.get("translations"):
            raise ValueError("DeepL API returned no translations")

        return result["translations"][0]["text"]

    def translate_texts(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
    ) -> List[str]:
        """
        Translate multiple texts in a single DeepL API call.

        Args:
            texts: List of texts to translate.
            target_lang: Target language code.
            source_lang: Optional source language code.
            formality: Optional formality preference.

        Returns:
            List of translated texts.
        """
        if target_lang not in SUPPORTED_DEEPL_LANGUAGES:
            raise ValueError(f"Unsupported target language: {target_lang}")

        payload: Dict[str, str] = {
            "target_lang": target_lang.upper(),
        }

        if source_lang:
            payload["source_lang"] = source_lang.upper()
        if formality:
            payload["formality"] = formality

        for text in texts:
            payload["text"] = payload.get("text", "") + "\x00" + text if payload.get("text") else text

        response = self.session.post(
            f"{self.base_url}/translate",
            data=payload,
        )
        response.raise_for_status()
        result = response.json()

        return [t["text"] for t in result.get("translations", [])]


def translate_compliance_note(
    note: ComplianceNote,
    api_key: Optional[str] = None,
    use_free_api: bool = False,
) -> ComplianceNote:
    """
    Translate a compliance note to the target language using DeepL API.

    Uses the DeepL Neural Machine Translation engine at api.deepl.com
    to translate encryption/compliance notes for international reviewers.

    Args:
        note: ComplianceNote with original text and target language.
        api_key: Optional DeepL API key (falls back to DEEPL_API_KEY env var).
        use_free_api: Use api-free.deepl.com endpoint for free tier.

    Returns:
        ComplianceNote with translated text in original_text field.
    """
    client = DeepLClient(api_key=api_key, use_free_api=use_free_api)

    translated = client.translate_text(
        text=note.original_text,
        target_lang=note.target_language,
        source_lang=note.source_language if note.source_language else None,
    )

    return ComplianceNote(
        note_id=note.note_id,
        original_text=translated,
        source_language=note.source_language,
        target_language=note.target_language,
        compliance_standard=note.compliance_standard,
    )


def translate_compliance_notes_batch(
    notes: List[ComplianceNote],
    api_key: Optional[str] = None,
    use_free_api: bool = False,
) -> List[ComplianceNote]:
    """
    Translate a batch of compliance notes using DeepL API.

    Groups notes by target language for efficient translation
    via the DeepL batch translation endpoint.

    Args:
        notes: List of ComplianceNote objects to translate.
        api_key: Optional DeepL API key.
        use_free_api: Use free tier endpoint.

    Returns:
        List of translated ComplianceNote objects.
    """
    client = DeepLClient(api_key=api_key, use_free_api=use_free_api)

    grouped: Dict[str, List[int]] = {}
    for i, note in enumerate(notes):
        target = note.target_language.upper()
        if target not in grouped:
            grouped[target] = []
        grouped[target].append(i)

    results = list(notes)

    for target_lang, indices in grouped.items():
        texts = [notes[i].original_text for i in indices]

        source_lang = notes[indices[0]].source_language
        if source_lang:
            source_lang = source_lang.upper()

        translated = client.translate_texts(
            texts=texts,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        for idx, translated_text in zip(indices, translated):
            results[idx] = ComplianceNote(
                note_id=notes[idx].note_id,
                original_text=translated_text,
                source_language=notes[idx].source_language,
                target_language=notes[idx].target_language,
                compliance_standard=notes[idx].compliance_standard,
            )

    return results


if __name__ == "__main__":
    sample_note = ComplianceNote(
        note_id="note-001",
        original_text="The encryption key rotation policy requires all AES-256 keys to be rotated every 90 days per SOC 2 compliance requirements.",
        source_language="EN",
        target_language="DE",
        compliance_standard="SOC 2",
    )

    try:
        translated = translate_compliance_note(sample_note)
        print(f"Original ({sample_note.source_language}): {sample_note.original_text}")
        print(f"Translated ({translated.target_language}): {translated.original_text}")
    except Exception as e:
        print(f"Translation failed (ensure DEEPL_API_KEY is set): {e}")
