import json
import os
from typing import Dict, Any
from identity_models import IdentityConfig
from identity_models import ClaimsNormalization

# ---- Provider name → translation map ----
# In a real‑world service the translations would be stored in a database or i18n files.
# Here we demonstrate the pattern with a hard‑coded dictionary.
CONSENT_TRANSLATIONS: Dict[str, Dict[str, Dict[str, str]]] = {
    "IBM App ID": {
        "en": {
            "title": "Your consent for IBM App ID",
            "description": "By granting consent you allow IBM App ID to process your profile data for authentication.",
            "grant_button": "Allow Access",
        },
        "es": {
            "title": "Su consentimiento para IBM App ID",
            "description": "Al conceder el consentimiento, permite a IBM App ID procesar sus datos de perfil para la autenticación.",
            "grant_button": "Permitir acceso",
        },
        "fr": {
            "title": "Votre consentement pour IBM App ID",
            "description": "En accordant le consentement, vous autorisez IBM App ID à traiter vos données de profil pour l'authentification.",
            "grant_button": "Autoriser l'accès",
        },
    },
    "Auth0": {
        "en": {
            "title": "Auth0 Consent",
            "description": "Allow Auth0 to access your profile information for signing in.",
            "grant_button": "Allow",
        },
        "de": {
            "title": "Auth0 Zustimmung",
            "description": "Erlauben Sie Auth0 den Zugriff auf Ihre Profildaten zum Einloggen.",
            "grant_button": "Zustimmen",
        },
    },
    # Add more providers as needed
}


# ---- Helper to pick language (fallback to English) ----
def _get_language() -> str:
    return os.getenv("CONSENT_LANG", "en")


def translate_consent(provider: str) -> Dict[str, str]:
    """Return a dictionary of translated consent strings for the given provider.

    Args:
        provider (str): Recognised provider name (case‑insensitive).
    Returns:
        Dict[str, str]: Keys like `title`, `description`, `grant_button`.
    Raises:
        ValueError: Provider not found or language not supported.
    """
    provider = provider.capitalize()  # normalise to match keys
    lang = _get_language()
    config = CONSENT_TRANSLATIONS.get(provider)
    if not config:
        raise ValueError(f"Provider '{provider}' has no consent translations.")
    translation = config.get(lang)
    if not translation:
        # Fallback to English if the requested language is missing
        translation = config["en"]
    return translation


# Example usage (local testing) ----
if __name__ == "__main__":
    # Simulate a consent request for a provider
    mock_provider = "Auth0"  # could be 'IBM App ID' or any key present above
    try:
        translated = translate_consent(mock_provider)
        print(
            json.dumps(
                {
                    "provider": mock_provider,
                    "language": _get_language(),
                    "consent_text": translated,
                },
                indent=2,
            )
        )
    except Exception as err:
        print(json.dumps({"error": str(err)}))
