# Local configuration and helper utilities for Streaming Speech-to-Text

import os
from pathlib import Path
from typing import Optional

# Common provider selection (choose one at runtime)
PROVIDER = os.getenv(
    "STT_PROVIDER", "watson"
)  # options: watson, amazon, dashscope, google, azure, deepgram

# Shared helper to load API credentials


def get_credentials() -> Optional[dict]:
    """Return a dict of credentials for the selected provider."""
    creds = {}
    if PROVIDER == "watson":
        creds["apikey"] = os.getenv("IBM_STT_APIKEY")
        creds["url"] = os.getenv("IBM_STT_URL")
    elif PROVIDER == "amazon":
        creds["access_key"] = os.getenv("AWS_ACCESS_KEY_ID")
        creds["secret_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        creds["region"] = os.getenv("AWS_REGION", "us-east-1")
    elif PROVIDER == "dashscope":
        creds["api_key"] = os.getenv("DASHSCOPE_API_KEY")
    elif PROVIDER == "google":
        creds["credentials_path"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    elif PROVIDER == "azure":
        creds["key"] = os.getenv("AZURE_SPEECH_KEY")
        creds["region"] = os.getenv("AZURE_SPEECH_REGION")
    elif PROVIDER == "deepgram":
        creds["api_key"] = os.getenv("DEEPGRAM_API_KEY")
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")
    return creds if all(creds.values()) else None


# Helper to normalize a generic streaming result into a unified schema


def normalize_result(raw: dict) -> dict:
    """Convert provider-specific streaming results to a common shape:
    {'transcript': str, 'is_final': bool}.
    """
    if "transcript" in raw and "is_final" in raw:
        return {"transcript": raw["transcript"], "is_final": bool(raw["is_final"])}
    elif "result" in raw and "alternatives" in raw["result"]:
        # e.g., Watson response shape
        alt = raw["result"]["alternatives"][0]
        return {"transcript": alt.get("transcript", "")}
    elif "partial" in raw or "final" in raw:
        # DashScope shape
        return {
            "transcript": raw.get("partial", raw.get("final", "")),
            "is_final": "final" in raw,
        }
    # Add more mappings as needed for other providers
    return {"transcript": "", "is_final": False}
