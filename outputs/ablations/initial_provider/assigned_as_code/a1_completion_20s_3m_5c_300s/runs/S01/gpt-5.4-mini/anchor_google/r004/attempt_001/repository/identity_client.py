import os
from dataclasses import dataclass


@dataclass
class IdentityConfig:
    project_id: str | None = None
    firebase_credentials_path: str | None = None
    openai_api_key: str | None = None
    firecrawl_api_key: str | None = None


def load_identity_config(config=None):
    config = config or {}
    return IdentityConfig(
        project_id=config.get("project_id") or os.getenv("FIREBASE_PROJECT_ID"),
        firebase_credentials_path=config.get("credentials_path") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        openai_api_key=config.get("openai_api_key") or os.getenv("OPENAI_API_KEY"),
        firecrawl_api_key=config.get("firecrawl_api_key") or os.getenv("FIRECRAWL_API_KEY"),
    )


def build_firebase_app(config=None):
    import firebase_admin

    identity_config = load_identity_config(config)
    try:
        return firebase_admin.get_app()
    except ValueError:
        return firebase_admin.initialize_app(options={"projectId": identity_config.project_id})


def build_openai_client(config=None):
    from openai import OpenAI

    identity_config = load_identity_config(config)
    return OpenAI(api_key=identity_config.openai_api_key)
