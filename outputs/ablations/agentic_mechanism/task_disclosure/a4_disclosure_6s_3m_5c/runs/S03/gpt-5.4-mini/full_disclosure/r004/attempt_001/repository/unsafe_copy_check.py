from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence

from openai import OpenAI


@dataclass(frozen=True)
class UnsafeCopyCheckConfig:
    api_key: str
    model: str = "gpt-5.4-mini"
    base_url: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None


@dataclass
class UnsafeCopyIssue:
    category: str
    severity: str
    message: str
    segment_index: Optional[int] = None
    excerpt: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnsafeCopyCheckRequest:
    localized_copy: Sequence[str]
    source_language: str
    target_language: str
    locale: Optional[str] = None
    policy: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnsafeCopyCheckResponse:
    is_safe: bool
    issues: List[UnsafeCopyIssue] = field(default_factory=list)
    summary: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


def load_unsafe_copy_check_config() -> UnsafeCopyCheckConfig:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("TRANSLATION_API_KEY")
    if not api_key:
        raise ValueError("Missing API key: set OPENAI_API_KEY or TRANSLATION_API_KEY")
    return UnsafeCopyCheckConfig(
        api_key=api_key,
        model=os.getenv("UNSAFE_COPY_CHECK_MODEL", "gpt-5.4-mini"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORGANIZATION"),
        project=os.getenv("OPENAI_PROJECT"),
    )


def build_unsafe_copy_check_client(config: Optional[UnsafeCopyCheckConfig] = None) -> OpenAI:
    cfg = config or load_unsafe_copy_check_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def check_unsafe_copy(
    request: UnsafeCopyCheckRequest,
    config: Optional[UnsafeCopyCheckConfig] = None,
) -> UnsafeCopyCheckResponse:
    cfg = config or load_unsafe_copy_check_config()
    client = build_unsafe_copy_check_client(cfg)
    text = "\n".join(request.localized_copy)
    response = client.responses.create(
        model=cfg.model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a safety reviewer for localized copy. Identify unsafe content such as "
                    "hate, harassment, sexual content, self-harm, violence, illegal instructions, "
                    "or policy-violating claims. Return concise JSON with is_safe, issues, and summary."
                ),
            },
            {
                "role": "user",
                "content": {
                    "type": "input_text",
                    "text": (
                        f"Source language: {request.source_language}\n"
                        f"Target language: {request.target_language}\n"
                        f"Locale: {request.locale or ''}\n"
                        f"Policy: {request.policy or ''}\n"
                        f"Copy:\n{text}"
                    ),
                },
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    payload = _extract_json_payload(response)
    return _normalize_response(payload)


def _extract_json_payload(response: Any) -> Mapping[str, Any]:
    output_text = getattr(response, "output_text", None)
    if output_text:
        import json

        return json.loads(output_text)
    if isinstance(response, Mapping):
        return response
    raise ValueError("Unable to extract JSON payload from response")


def _normalize_response(payload: Mapping[str, Any]) -> UnsafeCopyCheckResponse:
    issues_payload = payload.get("issues", []) or []
    issues = [
        UnsafeCopyIssue(
            category=str(item.get("category", "")),
            severity=str(item.get("severity", "")),
            message=str(item.get("message", "")),
            segment_index=item.get("segment_index"),
            excerpt=item.get("excerpt"),
            metadata=dict(item.get("metadata", {}) or {}),
        )
        for item in issues_payload
    ]
    return UnsafeCopyCheckResponse(
        is_safe=bool(payload.get("is_safe", not issues)),
        issues=issues,
        summary=str(payload.get("summary", "")),
        metadata=dict(payload.get("metadata", {}) or {}),
    )
