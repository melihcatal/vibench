import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4.1-mini"


class VisualSafetyTextClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = OPENAI_BASE_URL, model: str = OPENAI_MODEL):
        self.api_key = api_key or os.getenv(OPENAI_API_KEY_ENV)
        self.base_url = base_url.rstrip("/")
        self.model = model
        if not self.api_key:
            raise ValueError(f"Missing {OPENAI_API_KEY_ENV}")

    def check_labels(self, labels: List[str]) -> Dict[str, Any]:
        prompt = (
            "Review the following generated visual labels for unsafe, hateful, harassing, sexual, violent, or self-harm text. "
            "Return strict JSON with keys unsafe (boolean), risk_level (one of low, medium, high), and reasons (array of strings). "
            f"Labels: {labels}"
        )
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a safety classifier for visual label text."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return {"provider": "openai", "model": self.model, "raw": content}


def check_generated_visual_labels(labels: List[str], api_key: Optional[str] = None) -> Dict[str, Any]:
    return VisualSafetyTextClient(api_key=api_key).check_labels(labels)
