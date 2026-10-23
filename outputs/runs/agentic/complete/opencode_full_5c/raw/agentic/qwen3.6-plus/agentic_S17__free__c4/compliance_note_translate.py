import os
from typing import Optional, List, Dict
from datetime import datetime

import openai

from security_models import ComplianceNote

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"
OPENAI_API_HOST = "api.openai.com"

LANGUAGE_CODES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "it": "Italian",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
}


def translate_compliance_note(
    note_text: str,
    source_language: str = "en",
    target_language: str = "es",
    model: str = OPENAI_TRANSLATION_MODEL,
    api_key: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> ComplianceNote:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    source_lang_name = LANGUAGE_CODES.get(source_language, source_language)
    target_lang_name = LANGUAGE_CODES.get(target_language, target_language)

    system_prompt = (
        f"You are a professional translator specializing in cybersecurity, "
        f"encryption compliance, and regulatory documentation. "
        f"Translate the following text from {source_lang_name} to {target_lang_name}. "
        f"Preserve all technical terms, compliance references, and regulatory citations accurately. "
        f"Return only the translated text without additional commentary."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": note_text},
        ],
        temperature=0.3,
    )

    translated_text = response.choices[0].message.content.strip()

    return ComplianceNote(
        original_text=note_text,
        source_language=source_language,
        target_language=target_language,
        translated_text=translated_text,
        model=model,
        metadata=metadata,
    )


def translate_compliance_notes_batch(
    notes: List[Dict],
    target_language: str = "es",
    model: str = OPENAI_TRANSLATION_MODEL,
    api_key: Optional[str] = None,
) -> List[ComplianceNote]:
    results = []
    for note in notes:
        note_text = note.get("text", note.get("note", ""))
        source_language = note.get("source_language", "en")
        metadata = note.get("metadata")

        result = translate_compliance_note(
            note_text=note_text,
            source_language=source_language,
            target_language=target_language,
            model=model,
            api_key=api_key,
            metadata=metadata,
        )
        results.append(result)

    return results


def translate_encryption_policy(
    policy_text: str,
    target_languages: List[str],
    model: str = OPENAI_TRANSLATION_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, ComplianceNote]:
    translations = {}
    for target_lang in target_languages:
        result = translate_compliance_note(
            note_text=policy_text,
            source_language="en",
            target_language=target_lang,
            model=model,
            api_key=api_key,
            metadata={"document_type": "encryption_policy"},
        )
        translations[target_lang] = result
    return translations


def get_compliance_translation_report(
    note_text: str,
    target_languages: List[str],
    model: str = OPENAI_TRANSLATION_MODEL,
    api_key: Optional[str] = None,
) -> str:
    lines = [
        f"Compliance Note Translation Report",
        f"==================================",
        f"Original Text ({LANGUAGE_CODES.get('en', 'English')}):",
        f"  {note_text}",
        f"",
        f"Translations:",
    ]

    for target_lang in target_languages:
        result = translate_compliance_note(
            note_text=note_text,
            source_language="en",
            target_language=target_lang,
            model=model,
            api_key=api_key,
        )
        lang_name = LANGUAGE_CODES.get(target_lang, target_lang)
        lines.append(f"  [{lang_name}]: {result.translated_text}")

    return "\n".join(lines)


def detect_and_translate(
    note_text: str,
    target_language: str = "en",
    model: str = OPENAI_TRANSLATION_MODEL,
    api_key: Optional[str] = None,
) -> ComplianceNote:
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )

    detection_response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Detect the language of the following text. Return only the ISO 639-1 language code (e.g., en, es, fr, de, ja, zh).",
            },
            {"role": "user", "content": note_text},
        ],
        temperature=0.0,
        max_tokens=10,
    )

    detected_language = detection_response.choices[0].message.content.strip().lower()
    if detected_language not in LANGUAGE_CODES:
        detected_language = "en"

    return translate_compliance_note(
        note_text=note_text,
        source_language=detected_language,
        target_language=target_language,
        model=model,
        api_key=api_key,
        metadata={"detected_language": detected_language},
    )
