from google.cloud import aiplatform


def unsafe_copy_check(text: str) -> dict[str, object]:
    return {"provider": "google-cloud-aiplatform", "unsafe": "violence" in text.lower() or "hate" in text.lower()}
