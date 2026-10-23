import os
import json
from typing import List, Dict, Any, Optional
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential


def translate_compliance_note(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    if not endpoint:
        endpoint = os.getenv(
            "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
        )
    if not key:
        key = os.getenv("AZURE_TRANSLATOR_KEY")
    if not region:
        region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not key:
        raise ValueError(
            "Azure Translator key must be provided or set in AZURE_TRANSLATOR_KEY environment variable"
        )

    credential = AzureKeyCredential(key)
    client = TextTranslationClient(
        endpoint=endpoint, credential=credential, region=region
    )

    try:
        if source_language:
            response = client.translate(
                body=[InputTextItem(text=text)],
                to=[target_language],
                from_parameter=source_language,
            )
        else:
            response = client.translate(
                body=[InputTextItem(text=text)], to=[target_language]
            )

        translation = response[0] if response else None

        if translation and translation.translations:
            translated_text = translation.translations[0].text
            detected_language = (
                translation.detected_language.language
                if translation.detected_language
                else source_language
            )

            return {
                "original_text": text,
                "translated_text": translated_text,
                "target_language": target_language,
                "source_language": detected_language,
                "provider": "Azure AI Translator",
                "success": True,
            }
        else:
            return {
                "original_text": text,
                "error": "No translation returned",
                "success": False,
            }
    except Exception as e:
        raise RuntimeError(f"Azure Translator API call failed: {e}")


def translate_encryption_notes(
    notes: List[Dict[str, Any]],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[Dict[str, Any]]:
    translated_notes = []

    for note in notes:
        note_text = note.get("note", "")
        note_id = note.get("id", "")

        try:
            translation_result = translate_compliance_note(
                text=note_text,
                target_language=target_language,
                source_language=source_language,
            )

            translated_note = note.copy()
            translated_note["translated_note"] = translation_result["translated_text"]
            translated_note["translation_metadata"] = {
                "target_language": target_language,
                "source_language": translation_result["source_language"],
                "provider": translation_result["provider"],
            }
            translated_notes.append(translated_note)
        except Exception as e:
            translated_note = note.copy()
            translated_note["translation_error"] = str(e)
            translated_notes.append(translated_note)

    return translated_notes


def batch_translate_compliance_documents(
    documents: List[Dict[str, Any]],
    target_language: str,
    fields_to_translate: List[str] = ["content", "description", "notes"],
) -> List[Dict[str, Any]]:
    translated_documents = []

    for doc in documents:
        translated_doc = doc.copy()
        translated_doc["translations"] = {}
        translated_doc["translation_metadata"] = {
            "target_language": target_language,
            "translated_fields": [],
            "provider": "Azure AI Translator",
        }

        for field in fields_to_translate:
            if field in doc and isinstance(doc[field], str) and doc[field].strip():
                try:
                    translation_result = translate_compliance_note(
                        text=doc[field], target_language=target_language
                    )

                    if translation_result["success"]:
                        translated_doc["translations"][field] = translation_result[
                            "translated_text"
                        ]
                        translated_doc["translation_metadata"][
                            "translated_fields"
                        ].append(field)
                except Exception as e:
                    translated_doc["translations"][field] = (
                        f"Translation failed: {str(e)}"
                    )

        translated_documents.append(translated_doc)

    return translated_documents


def detect_language(text: str) -> Dict[str, Any]:
    endpoint = os.getenv(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not key:
        raise ValueError(
            "Azure Translator key must be provided or set in AZURE_TRANSLATOR_KEY environment variable"
        )

    credential = AzureKeyCredential(key)
    client = TextTranslationClient(
        endpoint=endpoint, credential=credential, region=region
    )

    try:
        response = client.detect_language(body=[InputTextItem(text=text)])

        if response and response[0]:
            detection = response[0]
            return {
                "text": text,
                "detected_language": detection.language,
                "confidence_score": detection.confidence,
                "provider": "Azure AI Translator",
                "success": True,
            }
        else:
            return {
                "text": text,
                "error": "Language detection failed",
                "success": False,
            }
    except Exception as e:
        raise RuntimeError(f"Azure Translator language detection failed: {e}")


def translate_for_reviewer(
    compliance_note: str,
    reviewer_language: str = "en",
    note_language: Optional[str] = None,
) -> Dict[str, Any]:
    if not note_language:
        detection_result = detect_language(compliance_note)
        if detection_result["success"]:
            note_language = detection_result["detected_language"]
        else:
            note_language = "en"

    if note_language == reviewer_language:
        return {
            "original_note": compliance_note,
            "translated_note": compliance_note,
            "note_language": note_language,
            "reviewer_language": reviewer_language,
            "translation_required": False,
            "provider": "Azure AI Translator",
        }

    translation_result = translate_compliance_note(
        text=compliance_note,
        target_language=reviewer_language,
        source_language=note_language,
    )

    return {
        "original_note": compliance_note,
        "translated_note": translation_result["translated_text"],
        "note_language": note_language,
        "reviewer_language": reviewer_language,
        "translation_required": True,
        "provider": "Azure AI Translator",
        "translation_metadata": translation_result,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        text = sys.argv[1]
        target_lang = sys.argv[2]
        source_lang = sys.argv[3] if len(sys.argv) > 3 else None

        try:
            result = translate_compliance_note(text, target_lang, source_lang)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
