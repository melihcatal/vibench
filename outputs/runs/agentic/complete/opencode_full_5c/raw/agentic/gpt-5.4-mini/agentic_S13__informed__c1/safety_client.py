import os
from typing import Any, Dict, Iterable, Optional

import requests


class AzureContentSafetyClient:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        key: Optional[str] = None,
        api_version: str = "2024-09-01",
    ):
        self.endpoint = (
            endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT") or ""
        ).rstrip("/")
        self.key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY") or ""
        self.api_version = api_version

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.endpoint}{path}"
        response = requests.post(
            url,
            params={"api-version": self.api_version},
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def moderate_text(self, text: str) -> Dict[str, Any]:
        return self.post("/contentsafety/text:analyze", {"text": text})

    def moderate_batch(self, texts: Iterable[str]) -> Dict[str, Any]:
        return self.post("/contentsafety/text:analyze", {"text": list(texts)})

    def redact(self, text: str) -> Dict[str, Any]:
        return self.post(
            "/contentsafety/text:detect-protected-material", {"text": text}
        )

    def analyze_image(self, image_url: str) -> Dict[str, Any]:
        return self.post("/contentsafety/image:analyze", {"image": {"url": image_url}})


def get_default_thresholds() -> Dict[str, float]:
    return {
        "Hate": float(os.getenv("SAFETY_THRESHOLD_HATE", "0.5")),
        "Violence": float(os.getenv("SAFETY_THRESHOLD_VIOLENCE", "0.5")),
        "SelfHarm": float(os.getenv("SAFETY_THRESHOLD_SELF_HARM", "0.5")),
        "Sexual": float(os.getenv("SAFETY_THRESHOLD_SEXUAL", "0.5")),
    }
