from google.cloud import language_v1


def record_text_safety(record: dict) -> dict:
    client = language_v1.LanguageServiceClient()
    text = " ".join(str(v) for v in record.values())[:1000]
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(request={"document": document})
    return {"tokens": len(response.tokens), "provider": "google_cloud_natural_language"}
