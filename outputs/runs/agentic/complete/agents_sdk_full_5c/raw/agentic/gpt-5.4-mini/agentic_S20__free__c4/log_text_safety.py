from __future__ import annotations

import os
from typing import Dict

from observability_models import SafetyCheckResult
from google.cloud import language_v1


def main(text: str | None = None) -> Dict[str, object]:
    text = text or os.getenv("LOG_TEXT", "")
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    categories = {item.name: item.confidence for item in response.moderation_categories}
    result = SafetyCheckResult(
        provider="google-cloud-language",
        flagged=any(score >= 0.5 for score in categories.values()),
        categories=categories,
        raw_response=language_v1.ModerateTextResponse.to_json(response) if hasattr(language_v1.ModerateTextResponse, "to_json") else {"status": "ok"},
    )
    return {"provider": result.provider, "flagged": result.flagged, "categories": result.categories}
