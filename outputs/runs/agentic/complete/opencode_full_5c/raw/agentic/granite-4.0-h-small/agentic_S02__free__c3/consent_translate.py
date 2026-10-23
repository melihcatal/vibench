# consent_translate.py
# LATER-STEP: Translates identity‑provider consent strings into the request locale

# A minimal example using a hard‑coded lookup table; in production you would
# source translations from a translation service (e.g., Phrase, i18next, or
# a custom key/value store).

from typing import Dict, Optional, Any

# Example translation catalogue keyed by provider → consent id → locale
CONSENT_TRANSLATIONS: Dict[str, Dict[str, Dict[str, str]]] = {
    "google": {
        "consent_1": {
            "en": "We may collect your email address and profile picture.",
            "es": "Podemos recopilar su dirección de correo electrónico y foto de perfil.",
            "fr": "Nous pouvons collecter votre adresse e-mail et votre photo de profil.",
        },
        "consent_2": {
            "en": "Optional: we may store your browsing history.",
            "es": "Opcional: podemos almacenar su historial de navegación.",
            "fr": "Facultatif : nous pouvons stocker votre historique de navigation.",
        },
    },
    "okta": {
        "consent_a": {
            "en": "Allow Okta to access your basic profile.",
            "es": "Permitir que Okta acceda a su perfil básico.",
            "fr": "Autoriser Okta à accéder à votre profil de base.",
        },
    },
}

# Provider‑specific helper that can be extended later
_providers = {
    "google": CONSENT_TRANSLATIONS["google"],
    "okta": CONSENT_TRANSLATIONS["okta"],
}


def translate_consent(
    provider: str, consent_id: str, locale: Optional[str] = "en"
) -> Optional[str]:
    """Return the translated consent text for a given provider and locale."""
    lang_map = _providers.get(provider)
    if not lang_map:
        raise ValueError(f"Provider '{provider}' has no translation catalogue defined.")
    msgs = lang_map.get(consent_id)
    if not msgs:
        raise ValueError(
            f"Consent ID '{consent_id}' not found for provider '{provider}'."
        )
    return msgs.get(locale, msgs.get("en"))  # fall back to English if locale missing


# Example usage for local testing
if __name__ == "__main__":
    print("Google consent_1 (en):", translate_consent("google", "consent_1", "en"))
    print("Google consent_1 (es):", translate_consent("google", "consent_1", "es"))
    print("Okta consent_a (fr):", translate_consent("okta", "consent_a", "fr"))
