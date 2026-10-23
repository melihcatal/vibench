"""
Translate identity-provider consent copy using the AWS Translate service.

Translates OAuth/OIDC consent screen text (terms, privacy notices,
permissions descriptions) from identity providers into the user's
preferred locale using Amazon Translate.
"""

import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
TRANSLATE_TERMINOLOGY_NAME = os.environ.get(
    "AWS_TRANSLATE_IDENTITY_TERMS",
    "federated-login-consent-terms",
)


class TranslationError(Exception):
    """Raised when translation via AWS Translate fails."""
    pass


def create_translate_client(region: Optional[str] = None):
    """Create a boto3 Amazon Translate client."""
    return boto3.client(
        "translate",
        region_name=region or AWS_REGION,
    )


def translate_consent_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate consent screen text using Amazon Translate.

    Supports automatic source language detection and translation
    of identity provider consent copy (terms of service, privacy
    notices, scope descriptions) from any supported source language
    into the user's preferred locale.

    Amazon Translate supports languages including: en, es, fr, de,
    ja, ko, zh, pt, ar, hi, it, nl, pl, ru, tr, and many more.

    Args:
        text: The consent text to translate.
        source_language: Source language code (or "auto" for detection).
        target_language: Target language code.
        region: AWS region for the Translate service.

    Returns:
        Dict with translated text, detected source language, and metadata.
    """
    client = create_translate_client(region)

    try:
        params = {
            "Text": text,
            "TargetLanguageCode": target_language,
        }
        if source_language != "auto":
            params["SourceLanguageCode"] = source_language

        response = client.translate_text(**params)

        return {
            "translated_text": response["TranslatedText"],
            "source_language": response["SourceLanguageCode"],
            "target_language": response["TargetLanguageCode"],
            "original_text": text,
        }

    except ClientError as exc:
        raise TranslationError(
            f"Amazon Translate failed: {exc.response['Error']['Message']}"
        ) from exc


def translate_consent_scopes(
    scopes: Dict[str, str],
    target_language: str = "en",
    region: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate OAuth scope descriptions into the target language.

    Identity providers often return scope descriptions in their
    native language (e.g., German for a German IdP). This function
    translates each scope description for display on the consent
    screen.
    """
    translated: Dict[str, str] = {}

    for scope_name, description in scopes.items():
        if not description:
            translated[scope_name] = description
            continue

        result = translate_consent_text(
            text=description,
            target_language=target_language,
            region=region,
        )
        translated[scope_name] = result["translated_text"]

    return translated


def translate_consent_bundle(
    consent_data: Dict[str, Any],
    target_language: str = "en",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a complete consent data bundle from an identity provider.

    Translates all user-facing consent text fields including:
    - Terms of service
    - Privacy policy summaries
    - Scope descriptions
    - Connection/provider display names
    - Custom consent messages

    Uses Amazon Translate for each text field, preserving the
    original structure of the consent bundle.
    """
    client = create_translate_client(region)
    translated: Dict[str, Any] = {}

    text_fields = [
        "terms_of_service",
        "privacy_policy",
        "privacy_notice",
        "consent_message",
        "provider_description",
        "connection_description",
        "custom_message",
    ]

    for field in text_fields:
        if field in consent_data and consent_data[field]:
            text = consent_data[field]
            if isinstance(text, str):
                result = translate_consent_text(
                    text=text,
                    target_language=target_language,
                    region=region,
                )
                translated[field] = result["translated_text"]
                translated[f"{field}_source_lang"] = result["source_language"]
            elif isinstance(text, list):
                translated[field] = []
                for item in text:
                    if isinstance(item, str):
                        result = translate_consent_text(
                            text=item,
                            target_language=target_language,
                            region=region,
                        )
                        translated[field].append(result["translated_text"])
                    else:
                        translated[field].append(item)

    if "scopes" in consent_data:
        translated["scopes"] = translate_consent_scopes(
            consent_data["scopes"],
            target_language=target_language,
            region=region,
        )

    for key, value in consent_data.items():
        if key not in translated and isinstance(value, str):
            result = translate_consent_text(
                text=value,
                target_language=target_language,
                region=region,
            )
            translated[key] = result["translated_text"]
        elif key not in translated:
            translated[key] = value

    return translated


def batch_translate_consent_texts(
    texts: List[str],
    target_language: str = "en",
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Batch translate multiple consent text strings.

    Processes each text through Amazon Translate individually and
    returns a list of translation results with source detection.
    Useful for translating multiple consent strings from different
    identity providers in a single call.
    """
    results = []
    for text in texts:
        if not text:
            results.append({
                "translated_text": text,
                "source_language": "unknown",
                "target_language": target_language,
                "original_text": text,
            })
            continue

        result = translate_consent_text(
            text=text,
            target_language=target_language,
            region=region,
        )
        results.append(result)

    return results


def translate_idp_display_name(
    provider_name: str,
    target_language: str = "en",
    region: Optional[str] = None,
) -> str:
    """
    Translate an identity provider's display name for the consent UI.

    Identity providers may return their display name in their
    native language. This translates it for the end user's locale.
    """
    result = translate_consent_text(
        text=provider_name,
        target_language=target_language,
        region=region,
    )
    return result["translated_text"]


if __name__ == "__main__":
    print("AWS Translate consent handler ready.")
    print(f"Region: {AWS_REGION}")
