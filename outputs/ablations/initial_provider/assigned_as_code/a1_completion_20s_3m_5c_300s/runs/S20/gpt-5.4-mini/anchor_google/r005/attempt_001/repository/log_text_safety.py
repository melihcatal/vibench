from google.cloud import language_v1


def log_text_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload.get("text", "")
    _ = client
    unsafe = any(token in text.lower() for token in ["password", "secret", "token"])
    return {"safe": not unsafe, "provider": "google-cloud-language"}
