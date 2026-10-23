import os

# Configure client credentials for a concrete third‑party translation provider.
# In this example we use DeepL's REST API.

# Provider identifier (DeepL)
PROVIDER_NAME = "deepl"
# API endpoint for the translation service
BASE_URL = "https://api.deepl.com/v2/translate"
# Set authentication token – retrieve from environment for security
API_KEY = os.getenv("DEEPL_API_KEY")


def create_client():
    """Return a configured requests.Session ready to call the provider."""
    import requests

    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session


# Helper to build a common request payload
def build_request_payload(text, target_lang, source_lang="EN"):
    return {
        "text": text,
        "target_lang": target_lang,
        "source_lang": source_lang,
    }
