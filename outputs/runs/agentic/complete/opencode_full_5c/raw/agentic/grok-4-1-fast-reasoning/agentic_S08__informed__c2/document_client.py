import os


def read_pdf_bytes(document_path: str) -> bytes:
    with open(document_path, "rb") as f:
        return f.read()


PROVIDER_ENVS = {
    "azure_di": [
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "AZURE_DOCUMENT_INTELLIGENCE_KEY",
    ],
    "mindee": ["MINDEE_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "anthropic": ["ANTHROPIC_API_KEY"],
    "google_genai": ["GOOGLE_API_KEY"],
    "perspective": ["PERSPECTIVE_API_KEY"],
    "deepl": ["DEEPL_AUTH_KEY"],
    "mongodb": ["MONGODB_ATLAS_URI"],
}


def validate_env(provider: str):
    envs = PROVIDER_ENVS.get(provider, [])
    missing = [e for e in envs if not os.getenv(e)]
    if missing:
        raise ValueError(f"Missing environment variables for {provider}: {missing}")
