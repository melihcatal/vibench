import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from safety_models import normalize_text


@dataclass
class SafetyClientConfig:
    endpoint: str
    api_key: str
    api_version: str = '2023-10-15-preview'


class AzureContentSafetyClient:
    def __init__(self, config: Optional[SafetyClientConfig] = None):
        self.config = config or SafetyClientConfig(
            endpoint=os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT', '').rstrip('/'),
            api_key=os.environ.get('AZURE_CONTENT_SAFETY_KEY', ''),
        )

    def _headers(self) -> Dict[str, str]:
        return {
            'Ocp-Apim-Subscription-Key': self.config.api_key,
            'Content-Type': 'application/json',
        }

    def moderate_text(self, text: str) -> Dict[str, Any]:
        payload = {'text': normalize_text(text)}
        url = f"{self.config.endpoint}/contentsafety/text:analyze?api-version={self.config.api_version}"
        return requests.post(url, headers=self._headers(), json=payload, timeout=30).json()

    def moderate_batch(self, texts):
        return [self.moderate_text(text) for text in texts]

    def redact_text(self, text: str) -> Dict[str, Any]:
        payload = {'text': normalize_text(text), 'outputType': 'FourPartText'}
        url = f"{self.config.endpoint}/contentsafety/text:shieldPrompt?api-version={self.config.api_version}"
        return requests.post(url, headers=self._headers(), json=payload, timeout=30).json()

    def threshold_allow(self, scores: Dict[str, float], thresholds: Dict[str, float]) -> bool:
        for category, score in scores.items():
            if score >= thresholds.get(category, 1.0):
                return False
        return True
