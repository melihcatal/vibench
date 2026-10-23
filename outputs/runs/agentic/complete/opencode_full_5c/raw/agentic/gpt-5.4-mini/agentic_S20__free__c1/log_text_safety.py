import os

from google.cloud import aiplatform


def is_safe(text: str) -> dict:
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    unsafe_markers = ["password", "secret", "token", "credit card"]
    lowered = text.lower()
    risk = any(marker in lowered for marker in unsafe_markers)
    return {
        "safe": not risk,
        "reason": "contains sensitive content" if risk else "clear",
    }


if __name__ == "__main__":
    is_safe("")
