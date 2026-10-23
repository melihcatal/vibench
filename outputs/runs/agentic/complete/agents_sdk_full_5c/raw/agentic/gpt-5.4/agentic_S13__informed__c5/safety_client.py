from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Optional

import requests


DEFAULT_API_VERSION = "2024-09-01"
DEFAULT_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


class AzureContentSafetyClient:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        key: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.endpoint = (endpoint or os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]).rstrip("/")
        self.key = key or os.environ["AZURE_CONTENT_SAFETY_KEY"]
        self.api_version = api_version
        self.session = session or requests.Session()

    @property
    def analyze_url(self) -> str:
        return f"{self.endpoint}/contentsafety/text:analyze?api-version={self.api_version}"

    def analyze_text(
        self,
        text: str,
        categories: Optional[Iterable[str]] = None,
        blocklist_names: Optional[Iterable[str]] = None,
        output_type: str = "FourSeverityLevels",
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": text,
            "categories": list(categories or DEFAULT_CATEGORIES),
            "outputType": output_type,
        }
        if blocklist_names:
            payload["blocklistNames"] = list(blocklist_names)
        response = self.session.post(
            self.analyze_url,
            headers={
                "Ocp-Apim-Subscription-Key": self.key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
