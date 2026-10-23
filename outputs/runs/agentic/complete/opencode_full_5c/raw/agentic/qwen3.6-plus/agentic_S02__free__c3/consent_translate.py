import os
import time
from typing import Any, Dict, List, Optional

from google.cloud import translate_v2 as translate

from identity_models import ConsentRecord, ConsentStatus, AuditEvent, AuditEventType


GOOGLE_TRANSLATE_API_KEY = os.environ.get("GOOGLE_TRANSLATE_API_KEY", "")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")


def get_translate_client() -> translate.Client:
    if GOOGLE_TRANSLATE_API_KEY:
        return translate.Client(developer_key=GOOGLE_TRANSLATE_API_KEY)
    return translate.Client()


def translate_consent_text(
    consent_text: str,
    target_language: str,
    source_language: str = "en",
    user_id: Optional[str] = None,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_translate_client()

    result = client.translate(
        consent_text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )

    translated = result.get("translatedText", consent_text)
    detected_source = result.get("detectedSourceLanguage", source_language)

    audit_event = AuditEvent(
        event_id=f"evt_{int(time.time() * 1000)}",
        event_type=AuditEventType.CONSENT_TRANSLATED,
        timestamp=time.time(),
        user_id=user_id,
        provider=provider or "google_translate",
        details={
            "source_language": detected_source,
            "target_language": target_language,
            "original_length": len(consent_text),
            "translated_length": len(translated),
        },
    )

    return {
        "success": True,
        "original_text": consent_text,
        "translated_text": translated,
        "source_language": detected_source,
        "target_language": target_language,
        "audit_event": audit_event.to_dict(),
        "provider": "google_translate",
    }


def translate_consent_scopes(
    scopes: List[str],
    target_language: str,
    source_language: str = "en",
) -> Dict[str, str]:
    client = get_translate_client()
    translations = {}

    for scope in scopes:
        result = client.translate(
            scope,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )
        translations[scope] = result.get("translatedText", scope)

    return translations


def localize_consent_record(
    consent_record: ConsentRecord,
    target_language: str,
) -> Dict[str, Any]:
    if consent_record.consent_text:
        translation_result = translate_consent_text(
            consent_text=consent_record.consent_text,
            target_language=target_language,
            user_id=consent_record.user_id,
            provider=consent_record.provider,
        )
        consent_record.translated_text = translation_result["translated_text"]
        consent_record.language = target_language

    if consent_record.scopes:
        scope_translations = translate_consent_scopes(
            scopes=consent_record.scopes,
            target_language=target_language,
        )
    else:
        scope_translations = {}

    return {
        "success": True,
        "consent_record": {
            "user_id": consent_record.user_id,
            "provider": consent_record.provider,
            "scopes": consent_record.scopes,
            "scope_translations": scope_translations,
            "status": consent_record.status.value,
            "consent_text": consent_record.consent_text,
            "translated_text": consent_record.translated_text,
            "language": consent_record.language,
        },
        "provider": "google_translate",
    }


def batch_translate_consent(
    texts: List[str],
    target_language: str,
    source_language: str = "en",
) -> List[Dict[str, str]]:
    client = get_translate_client()

    results = []
    for text in texts:
        result = client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )
        results.append(
            {
                "original": text,
                "translated": result.get("translatedText", text),
                "detected_source": result.get(
                    "detectedSourceLanguage", source_language
                ),
            }
        )

    return results


def get_supported_languages() -> List[Dict[str, str]]:
    client = get_translate_client()
    languages = client.get_languages()

    return [
        {
            "code": lang.get("language"),
            "name": lang.get("name"),
        }
        for lang in languages
    ]
