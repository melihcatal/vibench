import json

# Hard‑coded translation map for illustrative purposes (could be replaced with i18n service)
CONSENT_TRANSLATIONS = {
    "en": {
        "title": "Consent Required",
        "description": "We need your consent to access the following data: name, email, profile picture.",
        "approve": "Allow",
        "decline": "Deny"
    },
    "es": {
        "title": "Se Requiere Consentimiento",
        "description": "Necesitamos su consentimiento para acceder a los siguientes datos: nombre, correo, foto de perfil.",
        "approve": "Permitir",
        "decline": "Denegar"
    },
    "fr": {
        "title": "Consentement Requis",
        "description": "Nous avons besoin de votre consentement pour accéder aux informations suivantes : nom, email, photo de profil.",
        "approve": "Autoriser",
        "decline": "Refuser"
    }
}

# Provider‑specific consent copy (example: Google, Auth0, Okta)
PROVIDER_CONSENT = {
    "google": {"title": "Google Consent", "description": "Allow Google to share your profile"},
    "auth0": {"title": "Auth0 Consent", "description": "Allow Auth0 to share your identity information"},
    "okta": {"title": "Okta Consent", "description": "Allow Okta to share your user data"}
}

# Resolve the correct translation for a given locale

def translate_consent(provider: str, locale: str = "en") -> str:
    base = CONSENT_TRANSLATIONS.get(locale, CONSENT_TRANSLATIONS["en"])
    provider_info = PROVIDER_CONSENT.get(provider, {})
    # Combine generic and provider‑specific parts
    lines = [
        base["title"],
        PROVIDER_CONSENT.get(provider, {}).get("title", ""),
        base["description"],
        PROVIDER_CONSENT.get(provider, {}).get("description", "")
    ]
    return "\n".join([l for l in lines if l]).strip()

# Example end‑user UI payload generator

def build_consent_ui_payload(provider: str, locale: str = "en") -> dict:
    text = translate_consent(provider, locale)
    # The UI expects three fields: title, description, buttons (approve/decline)
    return {
        "title": text.title(),
        "description": text.description(),
        "buttons": [
            {"label": CONSENT_TRANSLATIONS[locale]["approve"], "action": "approve"},
            {"label": CONSENT_TRANSLATIONS[locale]["decline"], "action": "decline"}
        ]
    }

if __name__ == "__main__":
    # Demo: build consent UI for an English‑speaking user for Google
    payload = build_consent_ui_payload("google", "en")
    print(json.dumps(payload, indent=2))
