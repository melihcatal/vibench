import json
from deepmerge import always_merger


def translate_consent(copy_data, locale="en"):
    """
    Translates identity-provider consent copy using a static dictionary of translations.
    copy_data: dict where keys are language codes and values are the original copy strings.
    Returns the translated strings for the requested locale.
    Simple placeholder implementation; in real usage load translations from i18n files.
    """
    translations = {
        "en": {
            "scope_read_profile": "View your basic profile information.",
            "scope_email": "Access your email address.",
            "scope_openid": "Confirm your identity.",
        },
        "es": {
            "scope_read_profile": "Ver su información básica de perfil.",
            "scope_email": "Acceder a su dirección de correo electrónico.",
            "scope_openid": "Confirmar su identidad.",
        },
    }
    # Merge provider-specific consent strings with generic ones
    generic = translations.get("en", {})
    specific = translations.get(locale, {})
    merged = always_merger.merge(generic, specific)
    return merged
