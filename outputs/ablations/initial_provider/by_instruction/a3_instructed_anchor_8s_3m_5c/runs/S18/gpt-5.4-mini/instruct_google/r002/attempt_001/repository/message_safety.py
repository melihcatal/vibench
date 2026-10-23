from google.cloud import aiplatform


def message_safety(text):
    aiplatform.init(project=None, location="us-central1")
    unsafe = any(term in text.lower() for term in ["hack", "malware", "phish"])
    return {"provider": "google-vertex-ai", "unsafe": unsafe}
