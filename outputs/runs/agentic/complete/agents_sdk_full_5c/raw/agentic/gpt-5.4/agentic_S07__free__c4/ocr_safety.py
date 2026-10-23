from __future__ import annotations

from google.cloud import language_v1


UNSAFE_CATEGORIES = {"Toxic", "Insult", "Profanity", "Derogatory", "Violent"}


def check_ocr_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    findings = []
    flagged = False
    for category in response.moderation_categories:
        findings.append({"name": category.name, "confidence": category.confidence})
        if category.name in UNSAFE_CATEGORIES and category.confidence >= 0.5:
            flagged = True
    return {"provider": "google_cloud_natural_language", "flagged": flagged, "categories": findings}
