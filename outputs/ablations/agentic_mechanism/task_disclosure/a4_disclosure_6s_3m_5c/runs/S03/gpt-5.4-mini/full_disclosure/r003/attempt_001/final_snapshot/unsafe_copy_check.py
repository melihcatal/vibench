from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class UnsafeCopyFinding:
    issue: str
    severity: str
    text: str
    explanation: str


@dataclass
class UnsafeCopyCheckResult:
    unsafe: bool
    findings: List[UnsafeCopyFinding]
    raw_response: Dict[str, Any]


def _extract_output_text(response_json: Dict[str, Any]) -> str:
    output = response_json.get("output", [])
    parts: List[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, str):
                    parts.append(text)
    if parts:
        return "\n".join(parts)
    return response_json.get("output_text", "") or ""


def _normalize_findings(data: Any) -> List[UnsafeCopyFinding]:
    findings: List[UnsafeCopyFinding] = []
    if isinstance(data, dict):
        data = data.get("findings", [])
    if not isinstance(data, list):
        return findings
    for item in data:
        if not isinstance(item, dict):
            continue
        findings.append(
            UnsafeCopyFinding(
                issue=str(item.get("issue", "")),
                severity=str(item.get("severity", "")),
                text=str(item.get("text", "")),
                explanation=str(item.get("explanation", "")),
            )
        )
    return findings


def check_unsafe_copy(text: str, source_language: Optional[str] = None, target_language: Optional[str] = None) -> UnsafeCopyCheckResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = {
        "task": "Check localized copy for unsafe content.",
        "text": text,
        "source_language": source_language,
        "target_language": target_language,
        "return_schema": {
            "unsafe": "boolean",
            "findings": [
                {
                    "issue": "string",
                    "severity": "low|medium|high",
                    "text": "string",
                    "explanation": "string",
                }
            ],
        },
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "You are a translation safety reviewer. Identify unsafe, harmful, hateful, sexual, violent, self-harm, illegal, or policy-violating localized copy and return only valid JSON matching the requested schema.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": json.dumps(prompt, ensure_ascii=False),
                        }
                    ],
                },
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    response_json = response.json()
    output_text = _extract_output_text(response_json).strip()
    parsed: Dict[str, Any] = {}
    if output_text:
        parsed = json.loads(output_text)
    findings = _normalize_findings(parsed)
    unsafe = bool(parsed.get("unsafe", False)) or bool(findings)
    return UnsafeCopyCheckResult(unsafe=unsafe, findings=findings, raw_response=response_json)
