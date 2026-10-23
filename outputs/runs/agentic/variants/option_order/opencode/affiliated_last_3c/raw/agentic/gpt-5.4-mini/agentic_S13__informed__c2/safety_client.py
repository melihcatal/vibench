import os
from typing import Dict, Optional


def get_config() -> Dict[str, Optional[str]]:
    return {
        "endpoint": os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "key": os.getenv("AZURE_CONTENT_SAFETY_KEY"),
        "api_version": os.getenv("AZURE_CONTENT_SAFETY_API_VERSION", "2023-10-01"),
    }


def build_headers() -> Dict[str, str]:
    config = get_config()
    headers = {"Content-Type": "application/json"}
    if config["key"]:
        headers["Ocp-Apim-Subscription-Key"] = config["key"]
    return headers
