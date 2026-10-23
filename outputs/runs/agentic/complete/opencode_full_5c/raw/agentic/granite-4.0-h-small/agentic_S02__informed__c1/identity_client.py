import os
from typing import TypedDict, Literal


class IdentityClientConfig(TypedDict):
    PROVIDER_NAME: Literal[
        "cognito",
        "microsoft",
        "google",
        "alibaba",
        "ibm",
        "auth0",
    ]
    CLIENT_ID: str
    CLIENT_SECRET: str = ""
    ISSUER: str = ""
    AUTH_URI: str = ""
    TOKEN_URI: str = ""


# Default config for Google Identity Platform OIDC (used in same-scenario files)
def default_google_config() -> IdentityClientConfig:
    return {
        "PROVIDER_NAME": "google",
        "CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET", ""),
        "ISSUER": "https://accounts.google.com",
        "AUTH_URI": os.getenv(
            "GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/v2/auth"
        ),
        "TOKEN_URI": os.getenv(
            "GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"
        ),
    }


# Helper to load config from environment variables
def load_config(provider: str) -> IdentityClientConfig:
    if provider == "google":
        return default_google_config()
    # Add providers as needed; for now stub with placeholder values
    return {
        "PROVIDER_NAME": provider,
        "CLIENT_ID": os.getenv(f"{provider.upper()}_CLIENT_ID"),
        "CLIENT_SECRET": os.getenv(f"{provider.upper()}_CLIENT_SECRET", ""),
        "ISSUER": os.getenv(f"{provider.upper()}_ISSUER", ""),
        "AUTH_URI": os.getenv(f"{provider.upper()}_AUTH_URI", ""),
        "TOKEN_URI": os.getenv(f"{provider.upper()}_TOKEN_URI", ""),
    }
