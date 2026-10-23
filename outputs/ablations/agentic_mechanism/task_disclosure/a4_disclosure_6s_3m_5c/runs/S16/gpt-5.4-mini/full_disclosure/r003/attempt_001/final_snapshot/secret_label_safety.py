import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


_SUSPICIOUS_PATTERNS = (
    re.compile(r"\b(password|passwd|secret|token|apikey|api_key|private[-_ ]?key|credential)\b", re.IGNORECASE),
    re.compile(r"\b(prod(uction)?|live|critical|admin|root|master)\b", re.IGNORECASE),
    re.compile(r"\b(do not share|confidential|internal only|restricted)\b", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9+/]{32,}={0,2}"),
)


@dataclass(frozen=True)
class LabelSafetyFinding:
    field: str
    text: str
    matched_pattern: str


@dataclass(frozen=True)
class LabelSafetyResult:
    safe: bool
    findings: List[LabelSafetyFinding]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "safe": self.safe,
            "findings": [
                {"field": item.field, "text": item.text, "matched_pattern": item.matched_pattern}
                for item in self.findings
            ],
        }


def _get_secret_id(secret_id: Optional[str]) -> str:
    resolved = secret_id or os.environ.get("AWS_SECRET_ID") or os.environ.get("SECRET_ID")
    if not resolved:
        raise ValueError("Missing secret id")
    return resolved


def _get_region(region_name: Optional[str]) -> Optional[str]:
    return region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")


def _extract_labels_and_notes(secret_value: Dict[str, Any]) -> Dict[str, str]:
    candidates = {
        "label": secret_value.get("label") or secret_value.get("name") or secret_value.get("title") or "",
        "notes": secret_value.get("notes") or secret_value.get("description") or secret_value.get("comment") or "",
    }
    return {key: str(value) for key, value in candidates.items() if value is not None}


def _scan_text(field: str, text: str) -> List[LabelSafetyFinding]:
    findings: List[LabelSafetyFinding] = []
    for pattern in _SUSPICIOUS_PATTERNS:
        if pattern.search(text):
            findings.append(LabelSafetyFinding(field=field, text=text, matched_pattern=pattern.pattern))
    return findings


def check_secret_label_safety(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> LabelSafetyResult:
    client = boto3.client("secretsmanager", region_name=_get_region(region_name))
    response = client.get_secret_value(SecretId=_get_secret_id(secret_id))
    secret_string = response.get("SecretString")
    if not secret_string:
        raise ValueError("Secret does not contain a JSON payload")
    secret_value = json.loads(secret_string)
    if not isinstance(secret_value, dict):
        raise ValueError("Secret JSON must be an object")

    findings: List[LabelSafetyFinding] = []
    for field, text in _extract_labels_and_notes(secret_value).items():
        findings.extend(_scan_text(field, text))

    return LabelSafetyResult(safe=not findings, findings=findings)


def main() -> None:
    try:
        result = check_secret_label_safety()
    except (BotoCoreError, ClientError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
