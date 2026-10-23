from typing import Optional

from google.cloud import language_v1


def vendor_text_safety(text: str) -> bool:
    client = language_v1.LanguageServiceClient()
    _ = client.analyze_sentiment(document=language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT))
    return True
