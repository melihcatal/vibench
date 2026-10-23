from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass(frozen=True)
class QualityIssue:
    category: str
    severity: str
    message: str
    source_text: Optional[str] = None
    translated_text: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "category": self.category,
            "severity": self.severity,
            "message": self.message,
        }
        if self.source_text is not None:
            payload["source_text"] = self.source_text
        if self.translated_text is not None:
            payload["translated_text"] = self.translated_text
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class QualitySummary:
    summary: str
    issues: List[QualityIssue] = field(default_factory=list)
    score: Optional[float] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "summary": self.summary,
            "issues": [issue.to_payload() for issue in self.issues],
        }
        if self.score is not None:
            payload["score"] = self.score
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


class OpenAIQualitySummaryClient:
    def __init__(self, api_key: str, base_url: str = OPENAI_API_BASE, model: str = OPENAI_MODEL, timeout: float = 60.0):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})

    @property
    def chat_completions_url(self) -> str:
        return self.base_url + "/chat/completions"

    def summarize(self, source_text: str, translated_text: str, source_language: Optional[str] = None, target_language: Optional[str] = None, context: Optional[str] = None, issues: Optional[Sequence[Mapping[str, Any]]] = None) -> QualitySummary:
        prompt: Dict[str, Any] = {
            "source_text": source_text,
            "translated_text": translated_text,
        }
        if source_language is not None:
            prompt["source_language"] = source_language
        if target_language is not None:
            prompt["target_language"] = target_language
        if context is not None:
            prompt["context"] = context
        if issues is not None:
            prompt["existing_issues"] = list(issues)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You evaluate translation quality and return concise issue summaries as JSON."},
                {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
            ],
            "temperature": 0,
        }
        response = self._session.post(self.chat_completions_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        parsed_issues = [
            QualityIssue(
                category=item.get("category", "other"),
                severity=item.get("severity", "medium"),
                message=item.get("message", ""),
                source_text=item.get("source_text"),
                translated_text=item.get("translated_text"),
                metadata=dict(item.get("metadata") or {}),
            )
            for item in data.get("issues", [])
        ]
        return QualitySummary(
            summary=data.get("summary", ""),
            issues=parsed_issues,
            score=data.get("score"),
            metadata=dict(data.get("metadata") or {}),
        )


def load_quality_summary_client(api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None, timeout: Optional[float] = None) -> OpenAIQualitySummaryClient:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV, "")
    return OpenAIQualitySummaryClient(
        api_key=key,
        base_url=base_url or OPENAI_API_BASE,
        model=model or OPENAI_MODEL,
        timeout=timeout if timeout is not None else 60.0,
    )


def summarize_translation_quality(source_text: str, translated_text: str, source_language: Optional[str] = None, target_language: Optional[str] = None, context: Optional[str] = None, issues: Optional[Sequence[Mapping[str, Any]]] = None, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None, timeout: Optional[float] = None) -> QualitySummary:
    client = load_quality_summary_client(api_key=api_key, base_url=base_url, model=model, timeout=timeout)
    return client.summarize(source_text=source_text, translated_text=translated_text, source_language=source_language, target_language=target_language, context=context, issues=issues)
