from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import language_v2


DEFAULT_LANGUAGE_ENDPOINT = "language.googleapis.com"


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    client = language_v2.LanguageServiceClient(client_options={"api_endpoint": DEFAULT_LANGUAGE_ENDPOINT})
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    return {
        "provider": "Google Cloud Natural Language API",
        "endpoint": DEFAULT_LANGUAGE_ENDPOINT,
        "categories": [
            {"name": item.name, "confidence": item.confidence}
            for item in response.moderation_categories
        ],
        "text_length": len(text),
        "google_cloud_project": os.getenv("GOOGLE_CLOUD_PROJECT"),
    }
