"""
Translate onboarding copy into the user's locale using Google Cloud Translation API.

Provider: Google Cloud Translation API (google-cloud-translate)
Concrete provider signals: google.cloud.translate_v3, translate.googleapis.com,
                           GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT.
"""

import os
import logging
from typing import Optional, List, Dict, Any

from google.cloud import translate_v3 as translate


logger = logging.getLogger(__name__)

# Google Cloud Translation provider configuration
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-translate-project")
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

# Default onboarding copy templates in English
DEFAULT_ONBOARDING_COPY = {
    "welcome_title": "Welcome to Our Platform!",
    "welcome_subtitle": "Let's get you set up in just a few steps.",
    "profile_setup": "Complete your profile to personalize your experience.",
    "email_verification": "Please verify your email to activate your account.",
    "next_steps": "You're all set! Explore our features below.",
}


def translate_onboarding_copy(
    locale: str,
    custom_copy: Optional[Dict[str, str]] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate onboarding copy strings into the user's preferred locale.
    
    Uses Google Cloud Translation API v3 (Advanced) via the
    google-cloud-translate SDK. The API endpoint is:
    https://translate.googleapis.com/v3/projects/{project_id}/locations/{location}:translateText
    
    Args:
        locale: Target locale code (e.g., "es", "fr", "ja", "de").
        custom_copy: Optional dict of custom copy strings to translate.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict with success status and translated copy strings.
    """
    target_project = project_id or GOOGLE_CLOUD_PROJECT
    source_copy = custom_copy or DEFAULT_ONBOARDING_COPY
    
    texts_to_translate = list(source_copy.values())
    keys = list(source_copy.keys())
    
    try:
        client = translate.TranslationServiceClient()
        parent = client.common_location_path(target_project, GOOGLE_CLOUD_LOCATION)
        
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts_to_translate,
                "mime_type": "text/plain",
                "source_language_code": "en",
                "target_language_code": locale,
            }
        )
        
        translated_values = [
            translation.translated_text for translation in response.translations
        ]
        
        translated_copy = dict(zip(keys, translated_values))
        
        logger.info(
            "Google Cloud Translation API: translated %d strings to locale=%s (project: %s)",
            len(translated_copy),
            locale,
            target_project,
        )
        
        return {
            "success": True,
            "locale": locale,
            "copy": translated_copy,
            "provider": "google_cloud_translate",
            "model": "nmt",
        }
        
    except Exception as e:
        logger.error("Google Cloud Translation API error: %s", str(e))
        return {
            "success": False,
            "error": "TRANSLATION_ERROR",
            "message": str(e),
            "locale": locale,
            "fallback_copy": source_copy,
            "provider": "google_cloud_translate",
        }


def detect_and_translate(
    text: str,
    target_locale: str,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Detect the source language and translate text to the target locale.
    
    Uses Google Cloud Translation API v3 for both language detection
    and translation via the translate.googleapis.com endpoint.
    
    Args:
        text: The text to translate.
        target_locale: Target locale code.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict with detected language, translated text, and confidence.
    """
    target_project = project_id or GOOGLE_CLOUD_PROJECT
    
    try:
        client = translate.TranslationServiceClient()
        parent = client.common_location_path(target_project, GOOGLE_CLOUD_LOCATION)
        
        detect_response = client.detect_language(
            request={
                "parent": parent,
                "content": text,
                "mime_type": "text/plain",
            }
        )
        
        detected_language = detect_response.languages[0].language_code if detect_response.languages else "en"
        confidence = detect_response.languages[0].confidence if detect_response.languages else 0.0
        
        translate_response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": detected_language,
                "target_language_code": target_locale,
            }
        )
        
        translated_text = translate_response.translations[0].translated_text
        
        logger.info(
            "Google Cloud Translation: detected=%s -> target=%s (confidence=%.2f, project: %s)",
            detected_language,
            target_locale,
            confidence,
            target_project,
        )
        
        return {
            "success": True,
            "source_language": detected_language,
            "target_language": target_locale,
            "original": text,
            "translated": translated_text,
            "confidence": confidence,
            "provider": "google_cloud_translate",
        }
        
    except Exception as e:
        logger.error("Google Cloud Translation API detect/translate error: %s", str(e))
        return {
            "success": False,
            "error": "TRANSLATION_ERROR",
            "message": str(e),
            "provider": "google_cloud_translate",
        }


def batch_translate_onboarding(
    locales: List[str],
    custom_copy: Optional[Dict[str, str]] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate onboarding copy into multiple locales.
    
    Args:
        locales: List of target locale codes.
        custom_copy: Optional custom copy strings.
        project_id: Optional Google Cloud project ID.
        
    Returns:
        Dict mapping locale codes to their translated copy.
    """
    results = {}
    
    for locale in locales:
        result = translate_onboarding_copy(
            locale=locale,
            custom_copy=custom_copy,
            project_id=project_id,
        )
        results[locale] = result
    
    successful_locales = [loc for loc, res in results.items() if res.get("success")]
    
    logger.info(
        "Google Cloud Translation batch: %d/%d locales translated successfully",
        len(successful_locales),
        len(locales),
    )
    
    return {
        "success": len(successful_locales) > 0,
        "locales_translated": successful_locales,
        "results": results,
        "provider": "google_cloud_translate",
    }
