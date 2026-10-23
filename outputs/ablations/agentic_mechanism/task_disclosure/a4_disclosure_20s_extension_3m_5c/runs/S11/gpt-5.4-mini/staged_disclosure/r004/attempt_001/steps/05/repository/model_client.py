import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-5.4-mini"
    timeout: float = 60.0


def load_config(prefix: str = "MODEL_") -> ModelClientConfig:
    api_key = os.getenv(f"{prefix}API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing API key: set MODEL_API_KEY or OPENAI_API_KEY")
    base_url = os.getenv(f"{prefix}BASE_URL", "https://api.openai.com/v1")
    model = os.getenv(f"{prefix}MODEL", "gpt-5.4-mini")
    timeout = float(os.getenv(f"{prefix}TIMEOUT", "60"))
    return ModelClientConfig(api_key=api_key, base_url=base_url.rstrip("/"), model=model, timeout=timeout)


class ModelClient:
    def __init__(self, config: Optional[ModelClientConfig] = None) -> None:
        self.config = config or load_config()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self._session.post(
            f"{self.config.base_url}{path}",
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()

    def complete(self, prompt: str, *, temperature: float = 0.2, max_output_tokens: int = 256) -> str:
        payload = {
            "model": self.config.model,
            "input": prompt,
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }
        data = self._post("/responses", payload)
        output = data.get("output", [])
        texts = []
        for item in output:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text = content.get("text")
                    if text:
                        texts.append(text)
        if texts:
            return "".join(texts)
        return data.get("output_text", "")

    def health(self) -> bool:
        try:
            self._session.get(f"{self.config.base_url}/models/{self.config.model}", timeout=self.config.timeout).raise_for_status()
            return True
        except requests.RequestException:
            return False


def get_client() -> ModelClient:
    return ModelClient()
