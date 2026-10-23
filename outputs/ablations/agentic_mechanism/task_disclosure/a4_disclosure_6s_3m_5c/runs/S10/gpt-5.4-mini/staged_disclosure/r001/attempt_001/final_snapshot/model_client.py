import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL_FAMILY = os.getenv("MODEL_FAMILY", "gpt-5")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

MODEL_FAMILIES = {
    "gpt-5": "gpt-5.4-mini",
    "gpt-4.1": "gpt-4.1-mini",
    "o-series": "o4-mini",
}


@dataclass(frozen=True)
class ModelConfig:
    api_base: str = OPENAI_API_BASE
    api_key: str = OPENAI_API_KEY
    model_family: str = DEFAULT_MODEL_FAMILY
    model: str = DEFAULT_MODEL
    timeout: int = 60

    @property
    def resolved_model(self) -> str:
        return MODEL_FAMILIES.get(self.model_family, self.model)


def load_config() -> ModelConfig:
    return ModelConfig(
        api_base=os.getenv("OPENAI_API_BASE", OPENAI_API_BASE),
        api_key=os.getenv("OPENAI_API_KEY", OPENAI_API_KEY),
        model_family=os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY),
        model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        timeout=int(os.getenv("OPENAI_TIMEOUT", "60")),
    )


def select_model(model_family: Optional[str] = None) -> str:
    family = model_family or os.getenv("MODEL_FAMILY", DEFAULT_MODEL_FAMILY)
    return MODEL_FAMILIES.get(family, os.getenv("OPENAI_MODEL", DEFAULT_MODEL))


def build_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or os.getenv("OPENAI_API_KEY", OPENAI_API_KEY)
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def infer(prompt: str, model_family: Optional[str] = None, temperature: float = 0.2) -> str:
    config = load_config()
    model = select_model(model_family) or config.resolved_model
    response = requests.post(
        f"{config.api_base.rstrip('/')}/responses",
        headers=build_headers(config.api_key),
        json={
            "model": model,
            "input": prompt,
            "temperature": temperature,
        },
        timeout=config.timeout,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text:
        return output_text
    outputs = data.get("output", [])
    for item in outputs:
        content = item.get("content", []) if isinstance(item, dict) else []
        for part in content:
            text = part.get("text") if isinstance(part, dict) else None
            if isinstance(text, str) and text:
                return text
    return ""
