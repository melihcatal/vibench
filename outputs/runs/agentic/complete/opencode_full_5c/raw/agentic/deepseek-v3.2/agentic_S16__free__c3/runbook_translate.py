import os
import json
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate


def runbook_translate(
    runbook_text: str, target_language: str = "es", source_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate secret-rotation runbook notes using Google Cloud Translation API.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = translate.Client()

    try:
        if not runbook_text.strip():
            return {
                "provider": "google_cloud_translate",
                "project_id": project_id,
                "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
                "original_text": runbook_text,
                "translated_text": "",
                "target_language": target_language,
                "source_language": source_language,
                "character_count": 0,
                "translation_confidence": 1.0,
                "detected_language": source_language,
            }

        result = client.translate(
            runbook_text,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )

        translated_text = result["translatedText"]
        detected_language = result.get("detectedSourceLanguage", source_language)

        security_keywords = [
            "password",
            "secret",
            "key",
            "token",
            "credential",
            "rotate",
            "rotation",
            "expire",
            "expiration",
            "access",
            "permission",
            "privilege",
            "admin",
        ]

        keyword_analysis = []
        for keyword in security_keywords:
            original_count = runbook_text.lower().count(keyword)
            translated_count = translated_text.lower().count(keyword)

            if original_count > 0 or translated_count > 0:
                keyword_analysis.append(
                    {
                        "keyword": keyword,
                        "original_count": original_count,
                        "translated_count": translated_count,
                        "preserved": translated_count >= original_count,
                    }
                )

        sections = []
        if "\n\n" in runbook_text:
            sections = runbook_text.split("\n\n")
        elif "\n" in runbook_text:
            sections = runbook_text.split("\n")
        else:
            sections = [runbook_text]

        section_translations = []
        for i, section in enumerate(sections):
            if section.strip():
                section_result = client.translate(
                    section.strip(),
                    target_language=target_language,
                    source_language=source_language,
                )
                section_translations.append(
                    {
                        "section_index": i,
                        "original": section.strip(),
                        "translated": section_result["translatedText"],
                        "character_count": len(section.strip()),
                    }
                )

        character_count = len(runbook_text)
        word_count = len(runbook_text.split())

        translation_quality = "high"
        if character_count > 5000:
            translation_quality = "medium"
        if "{" in runbook_text and "}" in runbook_text:
            translation_quality = "medium"

        response = {
            "provider": "google_cloud_translate",
            "project_id": project_id,
            "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
            "original_text": runbook_text,
            "translated_text": translated_text,
            "target_language": target_language,
            "source_language": source_language,
            "detected_language": detected_language,
            "character_count": character_count,
            "word_count": word_count,
            "translation_confidence": 0.95,
            "translation_quality": translation_quality,
            "keyword_analysis": keyword_analysis,
            "section_translations": section_translations[:10],
            "model": "nmt",
            "format": "text",
        }

        security_warnings = []
        for analysis in keyword_analysis:
            if not analysis["preserved"] and analysis["original_count"] > 0:
                security_warnings.append(
                    {
                        "keyword": analysis["keyword"],
                        "warning": f"Security keyword '{analysis['keyword']}' may not be properly translated",
                        "original_occurrences": analysis["original_count"],
                        "translated_occurrences": analysis["translated_count"],
                    }
                )

        if security_warnings:
            response["security_warnings"] = security_warnings

        placeholder_check = []
        placeholder_patterns = ["${", "{{", "[[", "%(", "<%"]
        for pattern in placeholder_patterns:
            if pattern in runbook_text:
                original_placeholders = runbook_text.count(pattern)
                translated_placeholders = translated_text.count(pattern)
                placeholder_check.append(
                    {
                        "pattern": pattern,
                        "original_count": original_placeholders,
                        "translated_count": translated_placeholders,
                        "preserved": translated_placeholders >= original_placeholders,
                    }
                )

        if placeholder_check:
            response["placeholder_preservation"] = placeholder_check

        return response

    except Exception as e:
        if "PERMISSION_DENIED" in str(e):
            raise PermissionError(
                f"Permission denied for Google Cloud Translation API"
            ) from e
        elif "INVALID_ARGUMENT" in str(e):
            raise ValueError(f"Invalid translation request: {e}") from e
        else:
            raise RuntimeError(f"Error translating runbook: {e}") from e
