import os

from identity_models import IdentityConfig, normalize_email, normalize_locale


def load_identity_config(config=None):
    config = config or {}
    return IdentityConfig(
        project_id=config.get("project_id") or os.environ["FIREBASE_PROJECT_ID"],
        api_key=config.get("api_key") or os.environ.get("FIREBASE_WEB_API_KEY"),
        openai_api_key=config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY"),
        pinecone_api_key=config.get("pinecone_api_key") or os.environ.get("PINECONE_API_KEY"),
        supabase_url=config.get("supabase_url") or os.environ.get("SUPABASE_URL"),
        supabase_service_role_key=config.get("supabase_service_role_key") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY"),
    )


def normalized_payload(payload):
    payload = dict(payload)
    if "email" in payload:
        payload["email"] = normalize_email(payload["email"])
    if "locale" in payload:
        payload["locale"] = normalize_locale(payload["locale"])
    return payload
