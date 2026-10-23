import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-5.4-mini")


@dataclass
class SafetyFinding:
    category: str
    severity: str
    text: str = ""
    rationale: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    safe: bool
    risk_level: str
    findings: List[SafetyFinding] = field(default_factory=list)
    summary: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)


def _coerce_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts: List[str] = []
        for item in text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                value = item.get("text") or item.get("content") or item.get("value")
                if value is not None:
                    parts.append(str(value))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if isinstance(text, dict):
        if "text" in text:
            return _coerce_text(text["text"])
        if "pages" in text:
            return _coerce_text([page.get("text", "") for page in text.get("pages", []) if isinstance(page, dict)])
        value = text.get("content") or text.get("value")
        return str(value) if value is not None else json.dumps(text, ensure_ascii=False)
    return str(text)


def _extract_output_text(response_json: Dict[str, Any]) -> str:
    chunks: List[str] = []
    for item in response_json.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                chunks.append(content.get("text", ""))
    if chunks:
        return "".join(chunks).strip()
    if isinstance(response_json.get("output_text"), str):
        return response_json["output_text"].strip()
    return ""


def _parse_json_response(text: str) -> Dict[str, Any]:
    stripped = text.strip()
    if not stripped:
        return {}
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(stripped[start : end + 1])
            except json.JSONDecodeError:
                return {}
        return {}


def check_ocr_text_safety(text: Any, api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 120) -> SafetyCheckResult:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    source_text = _coerce_text(text)
    if not source_text.strip():
        return SafetyCheckResult(safe=True, risk_level="low", findings=[], summary="No text provided", raw_response={})

    payload: Dict[str, Any] = {
        "model": model or OPENAI_SAFETY_MODEL,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Review OCR-extracted document text for unsafe content. Identify violence, self-harm, illicit instructions, sexual content, hate, fraud, or other safety concerns. Return strict JSON with keys safe, risk_level, summary, findings.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Analyze the following OCR text:\n\n{source_text}",
                    }
                ],
            },
        ],
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    raw = response.json()
    parsed = _parse_json_response(_extract_output_text(raw))

    findings: List[SafetyFinding] = []
    for item in parsed.get("findings", []) if isinstance(parsed.get("findings", []), list) else []:
        if isinstance(item, dict):
            findings.append(
                SafetyFinding(
                    category=str(item.get("category", "unknown")),
                    severity=str(item.get("severity", "unknown")),
                    text=str(item.get("text", "")),
                    rationale=str(item.get("rationale", "")),
                    metadata={k: v for k, v in item.items() if k not in {"category", "severity", "text", "rationale"}},
                )
            )

    safe = bool(parsed.get("safe", not findings))
    risk_level = str(parsed.get("risk_level", "low" if safe else "medium"))
    summary = str(parsed.get("summary", ""))
    if not summary:
        summary = "No safety issues detected" if safe else "Safety issues detected"

    return SafetyCheckResult(safe=safe, risk_level=risk_level, findings=findings, summary=summary, raw_response=raw)
