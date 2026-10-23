from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from safety_models import ModerationRequest, normalize_text


DEFAULT_AZURE_CONTENT_SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def get_content_safety_client() -> ContentSafetyClient:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def build_moderation_request(
    text: str, language: str = "en", **metadata: Any
) -> ModerationRequest:
    return ModerationRequest(
        text=normalize_text(text), language=language, metadata=metadata
    )


def iter_text_items(
    texts: Iterable[str], language: str = "en"
) -> List[ModerationRequest]:
    return [build_moderation_request(text, language=language) for text in texts]


def category_severity_map(response: Any) -> Dict[str, float]:
    mapped: Dict[str, float] = {}
    for item in getattr(response, "categories_analysis", []) or []:
        mapped[str(getattr(item, "category", "unknown"))] = float(
            getattr(item, "severity", 0.0)
        )
    return mapped
