import os
import boto3
from typing import Dict, List, Optional, Union
from botocore.exceptions import ClientError


def translate_dashboard_notes(
    text: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate metric or dashboard notes for another locale using Amazon Translate.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        Dictionary with translation results
    """
    if not text:
        return {
            "original_text": "",
            "translated_text": "",
            "target_language": target_language,
            "source_language": source_language,
            "error": "Empty text provided",
        }

    try:
        translate_client = boto3.client(
            "translate", region_name=os.getenv("AWS_REGION", "us-east-1")
        )

        translate_args = {
            "Text": text,
            "SourceLanguageCode": source_language or "auto",
            "TargetLanguageCode": target_language,
        }

        response = translate_client.translate_text(**translate_args)

        result = {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "target_language": target_language,
            "source_language": response.get("SourceLanguageCode", source_language),
            "provider": "Amazon Translate",
            "applied_terminology_names": response.get("AppliedTerminologies", []),
            "character_count": len(text),
        }

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        raise RuntimeError(f"Amazon Translate error ({error_code}): {error_message}")
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {str(e)}")


def batch_translate_notes(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Translate multiple dashboard notes.

    Args:
        texts: List of texts to translate
        target_language: Target language code
        source_language: Source language code

    Returns:
        List of translation results
    """
    results = []

    for text in texts:
        try:
            result = translate_dashboard_notes(text, target_language, source_language)
            results.append(result)
        except Exception as e:
            results.append(
                {
                    "original_text": text,
                    "translated_text": "",
                    "target_language": target_language,
                    "source_language": source_language,
                    "error": str(e),
                }
            )

    return results


def translate_metric_metadata(
    metadata: Dict[str, str],
    target_language: str,
    fields_to_translate: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Translate metric metadata fields.

    Args:
        metadata: Dictionary of metric metadata
        target_language: Target language code
        fields_to_translate: List of field names to translate (defaults to all string fields)

    Returns:
        Dictionary with translated metadata
    """
    if fields_to_translate is None:
        fields_to_translate = list(metadata.keys())

    translated_metadata = metadata.copy()
    translation_results = {}

    for field in fields_to_translate:
        if field in metadata and isinstance(metadata[field], str):
            try:
                result = translate_dashboard_notes(
                    metadata[field], target_language, source_language="en"
                )

                if "translated_text" in result:
                    translated_metadata[field] = result["translated_text"]
                    translation_results[field] = {
                        "success": True,
                        "original": metadata[field],
                        "translated": result["translated_text"],
                        "source_language": result.get("source_language", "en"),
                    }
                else:
                    translation_results[field] = {
                        "success": False,
                        "error": result.get("error", "Translation failed"),
                        "original": metadata[field],
                    }

            except Exception as e:
                translation_results[field] = {
                    "success": False,
                    "error": str(e),
                    "original": metadata[field],
                }

    return {
        "original_metadata": metadata,
        "translated_metadata": translated_metadata,
        "target_language": target_language,
        "translation_results": translation_results,
        "provider": "Amazon Translate",
    }


def get_supported_languages() -> Dict[str, List[str]]:
    """
    Get list of languages supported by Amazon Translate.

    Returns:
        Dictionary with language lists
    """
    try:
        translate_client = boto3.client(
            "translate", region_name=os.getenv("AWS_REGION", "us-east-1")
        )

        response = translate_client.list_languages()

        languages = response.get("Languages", [])

        language_codes = [lang["LanguageCode"] for lang in languages]
        language_names = [lang.get("LanguageName", "") for lang in languages]

        return {
            "language_codes": language_codes,
            "language_names": language_names,
            "count": len(languages),
            "provider": "Amazon Translate",
        }

    except Exception as e:
        raise RuntimeError(f"Failed to get supported languages: {str(e)}")
