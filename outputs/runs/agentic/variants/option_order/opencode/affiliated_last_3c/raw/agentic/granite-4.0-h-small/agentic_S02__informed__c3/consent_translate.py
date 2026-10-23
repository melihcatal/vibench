import os
import json
from identity_client import IdentityClient
from identity_models import ConsentTranslationRequest, ConsentTranslationResponse

# Example identity-provider consent strings for Auth0
AUTH0_CONSENT_SCREEN = (
    "We need access to your email, profile, and offline_access scopes to log you in."
)


class TranslatedConsent(TypedDict):
    locale: str
    category: str
    translated_text: str


def consent_translate(locale: str) -> ConsentTranslationResponse:
    """Translate identity-provider consent copy using OpenAI Chat API (GPT) for demonstration.
    Returns a list of translated consent blocks.
    """
    request_payload = ConsentTranslationRequest(
        source_text=AUTH0_CONSENT_SCREEN,
        target_locale=locale,
    )
    response = IdentityClient.translate_consents(request_payload)
    return response.translations
