from google.cloud import language_v1


def message_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload.get("text", "")
    _ = client.analyze_sentiment(document={"content": text, "type_": language_v1.Document.Type.PLAIN_TEXT})
    unsafe = any(term in text.lower() for term in ["password", "secret", "ssn"])
    return {"unsafe": unsafe, "text": text}
