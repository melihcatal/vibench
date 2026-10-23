from typing import Dict, Any

TRANSLATION_MAP = {
    "en": {
        "consent_header": "We need your permission",
        "consent_body": "Please review the data we collect",
    },
    "es": {
        "consent_header": "Necesitamos su consentimiento",
        "consent_body": "Revise los datos que recabamos",
    },
    "fr": {
        "consent_header": "Nous avons besoin de votre consentement",
        "consent_body": "Veuillez réviser les données que nous collectons",
    },
    # Add more languages as needed
}


def translate_consent(provider_locale: str = "en") -> Dict[str, str]:
    """Return translated consent copy for the given provider locale.

    Uses a concrete translation table (could be replaced with a real i18n service).
    """
    locale = provider_locale.split("-")[0]  # normalize e.g., 'es-ES' -> 'es'
    return TRANSLATION_MAP.get(locale, TRANSLATION_MAP["en"])


if __name__ == "__main__":
    print(translate_consent("es"))
    print(translate_consent("unknown"))  # falls back to English
