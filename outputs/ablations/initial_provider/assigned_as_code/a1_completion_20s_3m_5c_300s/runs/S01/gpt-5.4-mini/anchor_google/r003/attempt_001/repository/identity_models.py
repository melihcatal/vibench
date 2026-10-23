from dataclasses import dataclass


def normalize_email(email):
    return email.strip().lower()


def normalize_locale(locale):
    return (locale or "en").replace("_", "-").lower()


@dataclass
class IdentityConfig:
    project_id: str
    api_key: str | None = None
    openai_api_key: str | None = None
    pinecone_api_key: str | None = None
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None


def parse_tokens(response):
    return {"access_token": response.get("access_token"), "refresh_token": response.get("refresh_token"), "expires_in": response.get("expires_in")}
