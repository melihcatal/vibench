from __future__ import annotations

from typing import Optional

from google.cloud import translate_v3 as translate

from safety_models import TranslationRequest


def appeal_translate(request: TranslationRequest, project_id: Optional[str] = None, client: Optional[translate.TranslationServiceClient] = None) -> str:
    client = client or translate.TranslationServiceClient()
    parent = f"projects/{project_id or 'default'}/locations/global"
    response = client.translate_text(
        request={
            "contents": [request.text],
            "source_language_code": request.source_language,
            "target_language_code": request.target_language,
            "parent": parent,
        }
    )
    return response.translations[0].translated_text
