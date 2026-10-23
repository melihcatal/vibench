import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI


@dataclass(frozen=True)
class SafetyCheckResult:
    safe: bool
    labels: List[str]
    score: float
    provider: str = "openai"
    model: str = "omni-moderation-latest"
    raw: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class SafetyCheckerConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "omni-moderation-latest"

    @classmethod
    def from_env(cls) -> "SafetyCheckerConfig":
        return cls(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
            model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        )


class PlatformOutputSafetyChecker:
    def __init__(self, config: Optional[SafetyCheckerConfig] = None) -> None:
        self.config = config or SafetyCheckerConfig.from_env()
        kwargs: Dict[str, Any] = {}
        if self.config.api_key:
            kwargs["api_key"] = self.config.api_key
        if self.config.base_url:
            kwargs["base_url"] = self.config.base_url
        self.client = OpenAI(**kwargs)

    def check(self, output_text: str) -> SafetyCheckResult:
        response = self.client.moderations.create(
            model=self.config.model,
            input=output_text,
        )
        result = response.results[0]
        labels = self._extract_labels(result)
        score = self._extract_score(result)
        safe = not bool(getattr(result, "flagged", False))
        raw = self._to_dict(response)
        return SafetyCheckResult(
            safe=safe,
            labels=labels,
            score=score,
            model=self.config.model,
            raw=raw,
        )

    def _extract_labels(self, result: Any) -> List[str]:
        labels: List[str] = []
        category_scores = getattr(result, "category_scores", None) or {}
        categories = getattr(result, "categories", None) or {}
        for name, flagged in categories.items():
            if flagged:
                labels.append(str(name))
        if not labels:
            labels.extend([str(name) for name, score in category_scores.items() if float(score) >= 0.5])
        return sorted(set(labels))

    def _extract_score(self, result: Any) -> float:
        category_scores = getattr(result, "category_scores", None) or {}
        if not category_scores:
            return 0.0
        return max(float(score) for score in category_scores.values())

    def _to_dict(self, response: Any) -> Dict[str, Any]:
        if hasattr(response, "model_dump"):
            return response.model_dump()
        if hasattr(response, "to_dict"):
            return response.to_dict()
        return {"response": str(response)}


def check_platform_output_safety(output_text: str, config: Optional[SafetyCheckerConfig] = None) -> SafetyCheckResult:
    return PlatformOutputSafetyChecker(config=config).check(output_text)
