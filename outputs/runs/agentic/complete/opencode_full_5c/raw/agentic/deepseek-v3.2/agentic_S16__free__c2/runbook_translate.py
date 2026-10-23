import boto3
import os
import json
from typing import Dict, List, Optional
from botocore.exceptions import ClientError


def translate_runbook_notes(
    runbook_text: str, target_language: str = "es"
) -> Dict[str, any]:
    """
    Translate secret-rotation runbook notes using Amazon Translate.

    Args:
        runbook_text: Runbook text to translate
        target_language: Target language code (default: 'es' for Spanish)

    Returns:
        Dictionary with translation results
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    # Initialize AWS Translate client
    translate_client = boto3.client(service_name="translate", region_name=region_name)

    try:
        # Detect source language
        detect_response = translate_client.detect_text(
            Text=runbook_text[:100]  # Sample for detection
        )
        source_language = detect_response["Languages"][0]["LanguageCode"]

        # Translate the text
        translate_response = translate_client.translate_text(
            Text=runbook_text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        result = {
            "original_text": runbook_text,
            "translated_text": translate_response["TranslatedText"],
            "source_language": source_language,
            "target_language": target_language,
            "character_count": len(runbook_text),
            "translated_character_count": len(translate_response["TranslatedText"]),
            "aws_translate_details": {
                "applied_terminologies": translate_response.get(
                    "AppliedTerminologies", []
                ),
                "applied_settings": translate_response.get("AppliedSettings", {}),
            },
        }

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "InvalidRequestException":
            raise Exception(f"Invalid translation request: {e}")
        elif error_code == "TextSizeLimitExceededException":
            raise Exception(f"Text size limit exceeded: {e}")
        elif error_code == "UnsupportedLanguagePairException":
            raise Exception(f"Unsupported language pair: {e}")
        else:
            raise Exception(f"AWS Translate error: {e}")


def translate_runbook_with_glossary(
    runbook_text: str,
    target_language: str = "es",
    glossary_terms: Optional[Dict[str, str]] = None,
) -> Dict[str, any]:
    """
    Translate runbook with custom glossary for technical terms.

    Args:
        runbook_text: Runbook text to translate
        target_language: Target language code
        glossary_terms: Dictionary of term translations (term -> translation)

    Returns:
        Dictionary with translation results including glossary usage
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    translate_client = boto3.client(service_name="translate", region_name=region_name)

    try:
        # Create terminology if glossary terms provided
        terminology_name = None
        if glossary_terms and len(glossary_terms) > 0:
            terminology_name = f"runbook_glossary_{target_language}"

            # Create terminology data
            terms_list = []
            for source, target in glossary_terms.items():
                terms_list.append({"SourceText": source, "TargetText": target})

            # Note: In production, you would create/import terminology first
            # For this example, we'll just note that glossary would be used

        # Translate with terminology reference if available
        translate_kwargs = {
            "Text": runbook_text,
            "SourceLanguageCode": "auto",
            "TargetLanguageCode": target_language,
            "Settings": {
                "Formality": "FORMAL",  # Use formal tone for runbooks
                "Profanity": "MASK",  # Mask any profanity
            },
        }

        if terminology_name:
            translate_kwargs["TerminologyNames"] = [terminology_name]

        translate_response = translate_client.translate_text(**translate_kwargs)

        result = {
            "original_text": runbook_text,
            "translated_text": translate_response["TranslatedText"],
            "target_language": target_language,
            "glossary_used": glossary_terms is not None and len(glossary_terms) > 0,
            "glossary_term_count": len(glossary_terms) if glossary_terms else 0,
            "translation_metadata": {
                "applied_settings": translate_response.get("AppliedSettings", {}),
                "source_language_code": translate_response.get(
                    "SourceLanguageCode", "auto"
                ),
            },
        }

        # Check for any untranslated technical terms
        if glossary_terms:
            untranslated_terms = []
            for term in glossary_terms.keys():
                if term.lower() in translate_response["TranslatedText"].lower():
                    untranslated_terms.append(term)
            result["untranslated_technical_terms"] = untranslated_terms

        return result

    except ClientError as e:
        raise Exception(f"AWS Translate error: {e}")


def create_multilingual_runbook(
    runbook_text: str, languages: List[str] = None
) -> Dict[str, Dict[str, str]]:
    """
    Create multilingual runbook translations.

    Args:
        runbook_text: Original runbook text
        languages: List of language codes to translate to

    Returns:
        Dictionary with translations for each language
    """
    if languages is None:
        languages = ["es", "fr", "de", "ja", "zh"]  # Common languages

    region_name = os.environ.get("AWS_REGION", "us-east-1")

    translate_client = boto3.client(service_name="translate", region_name=region_name)

    results = {}

    for lang in languages:
        try:
            translate_response = translate_client.translate_text(
                Text=runbook_text, SourceLanguageCode="auto", TargetLanguageCode=lang
            )

            results[lang] = {
                "translated_text": translate_response["TranslatedText"],
                "source_language": translate_response.get("SourceLanguageCode", "auto"),
                "character_count": len(translate_response["TranslatedText"]),
            }

        except ClientError as e:
            results[lang] = {"error": str(e), "translated_text": None}

    return results


def validate_runbook_translation(
    original: str, translated: str, source_lang: str = "en", target_lang: str = "es"
) -> Dict[str, any]:
    """
    Validate translation quality by back-translating.

    Args:
        original: Original text
        translated: Translated text
        source_lang: Source language code
        target_lang: Target language code

    Returns:
        Validation results
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    translate_client = boto3.client(service_name="translate", region_name=region_name)

    try:
        # Back-translate to check consistency
        back_translate_response = translate_client.translate_text(
            Text=translated,
            SourceLanguageCode=target_lang,
            TargetLanguageCode=source_lang,
        )

        back_translated = back_translate_response["TranslatedText"]

        # Simple similarity check (in production, use more sophisticated metrics)
        original_words = set(original.lower().split())
        back_translated_words = set(back_translated.lower().split())

        common_words = original_words.intersection(back_translated_words)
        similarity_score = len(common_words) / max(len(original_words), 1)

        validation_result = {
            "original_text": original,
            "translated_text": translated,
            "back_translated_text": back_translated,
            "similarity_score": similarity_score,
            "validation_passed": similarity_score > 0.5,  # Threshold
            "word_overlap": len(common_words),
            "total_original_words": len(original_words),
            "total_back_translated_words": len(back_translated_words),
        }

        return validation_result

    except ClientError as e:
        raise Exception(f"Failed to validate translation: {e}")


# Example runbook text for secret rotation
EXAMPLE_RUNBOOK = """
SECRET ROTATION RUNBOOK

1. PRE-ROTATION CHECKS
   - Verify current secret version in AWS Secrets Manager
   - Check for any pending rotations
   - Validate backup of current secret
   - Notify dependent services

2. ROTATION PROCEDURE
   - Generate new secret value
   - Store as AWSPENDING version
   - Update all applications to use new secret
   - Test applications with new secret
   - Promote AWSPENDING to AWSCURRENT

3. POST-ROTATION
   - Archive old secret version
   - Update documentation
   - Log rotation event
   - Verify monitoring alerts

4. ROLLBACK PROCEDURE
   - If issues detected, revert to AWSPREVIOUS
   - Update applications to use previous secret
   - Investigate and fix issues
   - Schedule new rotation attempt
"""

if __name__ == "__main__":
    try:
        translation = translate_runbook_notes(EXAMPLE_RUNBOOK, target_language="es")
        print(f"Translated to Spanish ({translation['character_count']} chars):")
        print(translation["translated_text"][:200] + "...")
    except Exception as e:
        print(f"Error: {e}")
