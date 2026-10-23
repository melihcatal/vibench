# consent_translate.py
# [LATER-STEP] Translate identity-provider consent copy for user presentation

import json
from typing import Dict, Any

# Example translation dictionaries for a few providers
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "google": {
        "title": "Google Account Access",
        "description": "We need permission to read your profile and email address so we can authenticate you.",
    },
    "okta": {
        "title": "Okta Authentication",
        "description": "Allow us to view your user information and sign you in securely.",
    },
    "azure_ad": {
        "title": "Microsoft Account Consent",
        "description": "We request access to your profile information to complete the login.",
    },
}


def translate_consent(provider: str, locale: str = "en") -> Dict[str, str]:
    """Return localized consent UI copy for the requested provider."""
    # In a real system this would load JSON/YAML files per locale, fallback to 'en'
    if provider not in TRANSLATIONS:
        raise ValueError(f"Unknown provider for consent translation: {provider}")
    return TRANSLATIONS[provider]


def render_consent_ui(provider: str, locale: str = "en") -> str:
    """Generate a simple HTML snippet containing the translated consent copy."""
    try:
        copy = translate_consent(provider, locale)
    except ValueError as exc:
        return f"<p>{str(exc)}</p>"
    html = f"""
    <div class=\"consent-banner\">
        <h2>{copy["title"]}</h2>
        <p>{copy["description"]}</p>
        <button onclick=\"proceedLogin()\">Accept & Continue</button>
    </div>"""
    return html


if __name__ == "__main__":
    # Demo: render Google consent in English
    print(render_consent_ui("google", locale="en"))
