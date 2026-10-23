import os
import json
from typing import Dict, List, Optional
from google.cloud import translate_v2 as translate
from identity_models import ConsentData


def initialize_google_translate():
    """Initialize Google Cloud Translation client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    return translate.Client()


def translate_consent_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """Translate consent text using Google Cloud Translation API."""
    client = initialize_google_translate()

    try:
        if source_language:
            result = client.translate(
                text, target_language=target_language, source_language=source_language
            )
        else:
            result = client.translate(text, target_language=target_language)

        return result["translatedText"]

    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")


def translate_consent_data(
    consent_data: ConsentData, target_language: str
) -> Dict[str, Any]:
    """Translate all consent screen text to target language."""
    translations = {}

    scopes_translation = translate_scopes(consent_data.scopes, target_language)
    if scopes_translation:
        translations["scopes"] = scopes_translation

    client_name_translation = translate_consent_text(
        consent_data.client_name, target_language
    )
    translations["client_name"] = client_name_translation

    if consent_data.privacy_policy_url:
        privacy_policy_text = f"Privacy Policy: {consent_data.privacy_policy_url}"
        translations["privacy_policy"] = translate_consent_text(
            privacy_policy_text, target_language
        )

    if consent_data.terms_of_service_url:
        tos_text = f"Terms of Service: {consent_data.terms_of_service_url}"
        translations["terms_of_service"] = translate_consent_text(
            tos_text, target_language
        )

    consent_template = generate_consent_template(consent_data)
    consent_translation = translate_consent_text(consent_template, target_language)
    translations["consent_template"] = consent_translation

    translations["target_language"] = target_language
    translations["provider"] = "google"
    translations["model"] = "translate_v2"

    return translations


def translate_scopes(scopes: List[str], target_language: str) -> Dict[str, str]:
    """Translate OAuth scopes to target language."""
    scope_translations = {}

    scope_descriptions = {
        "openid": "Verify your identity",
        "email": "Access your email address",
        "profile": "Access your basic profile information",
        "user:email": "Access your email addresses (GitHub)",
        "offline_access": "Access your data while you're not using the app",
        "calendar.readonly": "View your calendars (Google)",
        "contacts.readonly": "View your contacts (Google)",
        "drive.readonly": "View your Google Drive files",
        "user.read": "Read your profile (Microsoft)",
        "mail.read": "Read your mail (Microsoft)",
    }

    for scope in scopes:
        description = scope_descriptions.get(scope, f"Access: {scope}")
        translated_description = translate_consent_text(description, target_language)
        scope_translations[scope] = translated_description

    return scope_translations


def generate_consent_template(consent_data: ConsentData) -> str:
    """Generate consent screen template text."""
    template_parts = []

    template_parts.append(
        f"{consent_data.client_name} is requesting access to your account."
    )
    template_parts.append("")
    template_parts.append("This will allow the application to:")

    for scope in consent_data.scopes:
        scope_desc = get_scope_description(scope)
        template_parts.append(f"• {scope_desc}")

    template_parts.append("")
    template_parts.append("You can revoke this access at any time.")

    if consent_data.privacy_policy_url:
        template_parts.append(f"Privacy Policy: {consent_data.privacy_policy_url}")

    if consent_data.terms_of_service_url:
        template_parts.append(f"Terms of Service: {consent_data.terms_of_service_url}")

    return "\n".join(template_parts)


def get_scope_description(scope: str) -> str:
    """Get human-readable description for a scope."""
    scope_descriptions = {
        "openid": "Verify your identity",
        "email": "Access your email address",
        "profile": "Access your basic profile information",
        "user:email": "Access your email addresses",
        "offline_access": "Access your data while you're not using the app",
        "calendar.readonly": "View your calendars",
        "contacts.readonly": "View your contacts",
        "drive.readonly": "View your Google Drive files",
        "user.read": "Read your profile",
        "mail.read": "Read your mail",
    }

    return scope_descriptions.get(scope, f"Access: {scope}")


def detect_language(text: str) -> Dict[str, Any]:
    """Detect language of text using Google Cloud Translation API."""
    client = initialize_google_translate()

    try:
        result = client.detect_language(text)

        return {
            "language": result["language"],
            "confidence": result.get("confidence", 0.0),
            "provider": "google",
            "model": "translate_v2",
        }

    except Exception as e:
        raise Exception(f"Language detection failed: {str(e)}")


def get_supported_languages() -> List[Dict[str, str]]:
    """Get list of languages supported by Google Cloud Translation."""
    client = initialize_google_translate()

    try:
        languages = client.get_languages()

        return [
            {"code": lang["language"], "name": lang["name"], "provider": "google"}
            for lang in languages
        ]

    except Exception as e:
        raise Exception(f"Failed to get supported languages: {str(e)}")


def translate_consent_for_provider(
    provider: str, target_language: str
) -> Dict[str, Any]:
    """Generate provider-specific consent translations."""
    provider_consent_texts = {
        "google": {
            "title": "Google Account Access",
            "description": "This app wants to access your Google Account",
            "scopes": {
                "openid": "Verify your identity with Google",
                "email": "View your email address",
                "profile": "View your basic profile info",
            },
        },
        "microsoft": {
            "title": "Microsoft Account Access",
            "description": "This app wants to access your Microsoft Account",
            "scopes": {
                "openid": "Verify your identity with Microsoft",
                "email": "View your email address",
                "profile": "View your basic profile info",
            },
        },
        "github": {
            "title": "GitHub Account Access",
            "description": "This app wants to access your GitHub Account",
            "scopes": {"user:email": "View your email addresses"},
        },
    }

    if provider not in provider_consent_texts:
        raise ValueError(f"Unsupported provider: {provider}")

    provider_texts = provider_consent_texts[provider]
    translations = {}

    for key, text in provider_texts.items():
        if isinstance(text, str):
            translations[key] = translate_consent_text(text, target_language)
        elif isinstance(text, dict):
            translated_dict = {}
            for subkey, subtext in text.items():
                translated_dict[subkey] = translate_consent_text(
                    subtext, target_language
                )
            translations[key] = translated_dict

    translations["provider"] = provider
    translations["target_language"] = target_language
    translations["translation_provider"] = "google"

    return translations
