import os


def load_identity_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("FIREBASE_PROJECT_ID"),
        "tenant_id": config.get("tenant_id") or os.environ.get("FIREBASE_TENANT_ID"),
        "locale": config.get("locale") or os.environ.get("DEFAULT_LOCALE", "en"),
        "openai_api_key": config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY"),
        "openai_model": config.get("openai_model") or os.environ.get("OPENAI_MODEL", "gpt-5.4-mini"),
        "openai_org": config.get("openai_org") or os.environ.get("OPENAI_ORG"),
        "retool_api_key": config.get("retool_api_key") or os.environ.get("RETOOL_API_KEY"),
        "retool_base_url": config.get("retool_base_url") or os.environ.get("RETOOL_BASE_URL", "https://api.retool.com"),
        "collection_name": config.get("collection_name") or os.environ.get("PROFILE_NOTES_COLLECTION", "profile_notes"),
    }


def normalize_email_password_payload(payload):
    payload = payload or {}
    email = (payload.get("email") or payload.get("user_email") or "").strip().lower()
    password = payload.get("password") or payload.get("secret") or ""
    return {"email": email, "password": password}


def normalize_text_payload(payload):
    payload = payload or {}
    return {
        "text": (payload.get("text") or payload.get("content") or payload.get("bio") or "").strip(),
        "locale": (payload.get("locale") or payload.get("language") or "en").strip(),
        "user_id": (payload.get("user_id") or payload.get("uid") or "").strip(),
    }


def normalize_support_payload(payload):
    payload = payload or {}
    return {
        "user_id": (payload.get("user_id") or payload.get("uid") or "").strip(),
        "email": (payload.get("email") or "").strip().lower(),
        "status": (payload.get("status") or payload.get("state") or "unknown").strip(),
    }
