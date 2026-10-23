from google.cloud import language_v1

from security_models import normalize_payload_text


def payload_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_payload_text(text), type_=language_v1.Document.Type.PLAIN_TEXT)
    _ = client.analyze_sentiment(request={"document": document})
    unsafe = any(token in normalize_payload_text(text).lower() for token in ("secret", "password", "token"))
    return {"provider": "google", "unsafe": unsafe}


def main() -> None:
    payload_safety("")


if __name__ == "__main__":
    main()
