import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from openai import OpenAI


@dataclass
class SafetyConfig:
    openai_api_key: Optional[str] = None
    moderation_model: str = "omni-moderation-latest"
    batch_moderation_model: str = "omni-moderation-latest"
    redaction_model: str = "omni-moderation-latest"
    thresholds: Dict[str, float] = field(default_factory=lambda: {
        "sexual": 0.5,
        "hate": 0.5,
        "harassment": 0.5,
        "self_harm": 0.3,
        "violence": 0.5,
        "illicit": 0.5,
    })

    def merge_overrides(self, overrides: Dict[str, Any]) -> "SafetyConfig":
        merged = SafetyConfig(
            openai_api_key=overrides.get("openai_api_key", self.openai_api_key),
            moderation_model=overrides.get("moderation_model", self.moderation_model),
            batch_moderation_model=overrides.get("batch_moderation_model", self.batch_moderation_model),
            redaction_model=overrides.get("redaction_model", self.redaction_model),
            thresholds={**self.thresholds, **overrides.get("thresholds", {})},
        )
        return merged


def load_safety_config() -> SafetyConfig:
    return SafetyConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        moderation_model=os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        batch_moderation_model=os.getenv("OPENAI_BATCH_MODERATION_MODEL", "omni-moderation-latest"),
        redaction_model=os.getenv("OPENAI_REDACTION_MODEL", "omni-moderation-latest"),
    )


class ModerationProviderClient:
    def __init__(self, config: SafetyConfig):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)

    def moderate_text(self, text: str, user_id: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        response = self.client.moderations.create(
            model=self.config.moderation_model,
            input=text,
        )
        return response.model_dump()

    def moderate_batch(self, messages: List[str], user_id: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        response = self.client.moderations.create(
            model=self.config.batch_moderation_model,
            input=messages,
        )
        return response.model_dump()

    def redact_unsafe(self, text: str, user_id: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        response = self.client.moderations.create(
            model=self.config.redaction_model,
            input=text,
        )
        return response.model_dump()
