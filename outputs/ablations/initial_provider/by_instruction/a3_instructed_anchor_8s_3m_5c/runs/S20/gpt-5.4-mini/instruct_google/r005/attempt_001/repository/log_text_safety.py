import re

from google.cloud import language_v1


def log_text_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    _ = client.analyze_sentiment(request={"document": document})
    unsafe = bool(re.search(r"\b(password|secret|token|credit card)\b", text, re.IGNORECASE))
    return {"unsafe": unsafe, "provider": "google_cloud_natural_language"}
