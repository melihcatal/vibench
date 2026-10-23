import json
from typing import Optional

# Placeholder for a real translation service; here we use a simple map for demo
CONSENT_TRANSLATIONS = {
    "en": {
        "consent_title": "Consent for Federated Login",
        "prompt": "We need your permission to share your basic profile (name, email, picture) with our service.",
    },
    "es": {
        "consent_title": "Consentimiento para Inicio de Sesión Federado",
        "prompt": "Necesitamos su permiso para compartir su perfil básico (nombre, correo, foto) con nuestro servicio.",
    },
    "fr": {
        "consent_title": "Consentement pour Connexion Fédérée",
        "prompt": "Nous avons besoin de votre consentement pour partager vos informations de base (nom, e‑mail, photo) avec notre service.",
    },
    # Add more locales as needed
}


def translate_consent_copy(locale: str = "en") -> dict[str, str]:
    """Return translated consent UI strings for the requested locale."""
    template = CONSENT_TRANSLATIONS.get(locale, CONSENT_TRANSLATIONS["en"])
    return {
        "title": template["consent_title"],
        "prompt": template["prompt"],
    }


# Example usage for later‑step integration
if __name__ == "__main__":
    locale = os.getenv("CONSENT_LOCALE", "en")
    translation = translate_consent_copy(locale)
    audit_entry = {
        "event_type": "consent_translated",
        "locale": locale,
        "translation": translation,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    # In production, persist `audit_entry` to the document store
    print("Consent translation audit entry:", json.dumps(audit_entry, indent=2))
