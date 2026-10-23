from google.cloud import language_v1
from typing import Optional

def moderate_claim_text(text: Optional[str]) -> bool:
    if not text:
        return True
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)
    return not response.moderation_categories