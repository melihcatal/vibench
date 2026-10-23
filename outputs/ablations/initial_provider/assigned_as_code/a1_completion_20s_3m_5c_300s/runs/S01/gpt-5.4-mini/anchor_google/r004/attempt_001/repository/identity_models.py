def normalize_email(email):
    return (email or "").strip().lower()


def normalize_locale(locale):
    return (locale or "en").strip().lower().replace("_", "-")


def normalize_text(text):
    return " ".join((text or "").split()).strip()


def build_account_payload(payload):
    payload = payload or {}
    return {
        "email": normalize_email(payload.get("email")),
        "password": payload.get("password"),
        "locale": normalize_locale(payload.get("locale")),
        "display_name": normalize_text(payload.get("display_name")),
        "note": normalize_text(payload.get("note")),
    }
