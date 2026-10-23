import os

from google.cloud import aiplatform


def message_safety(text: str):
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_REGION", "us-central1"),
    )
    unsafe_terms = ["malware", "phishing", "credential", "exploit"]
    lowered = (text or "").lower()
    unsafe = any(term in lowered for term in unsafe_terms)
    return {
        "safe": not unsafe,
        "provider": "google-cloud-aiplatform",
        "reason": None if not unsafe else "policy_match",
    }
