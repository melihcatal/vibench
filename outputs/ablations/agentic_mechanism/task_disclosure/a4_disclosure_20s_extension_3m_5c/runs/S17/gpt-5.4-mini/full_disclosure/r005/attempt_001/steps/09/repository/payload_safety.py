import json
import os
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from google.cloud import aiplatform_v1


DEFAULT_PROVIDER = "google_cloud_vertex_ai"
DEFAULT_MODEL_ID = "gemini-1.5-flash-002"
DEFAULT_LOCATION = "us-central1"


@dataclass(frozen=True)
class SafetyFinding:
    category: str
    severity: str
    matched_text: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafetyResult:
    provider: str
    model_id: str
    is_safe: bool
    risk_level: str
    findings: List[SafetyFinding]
    explanation: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["findings"] = [finding.as_dict() for finding in self.findings]
        return data


def _build_prompt(payload: str) -> str:
    return (
        "Assess the following decrypted text payload for unsafe content. "
        "Return JSON with keys is_safe (boolean), risk_level (low|medium|high), "
        "findings (array of {category,severity,matched_text}), and explanation (string).\n\n"
        f"PAYLOAD:\n{payload}"
    )


def _extract_json(text: str) -> Dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("Model response did not contain JSON")
    return json.loads(match.group(0))


def _fallback_scan(payload: str) -> SafetyResult:
    patterns = [
        ("credentials", "high", r"(?i)\b(api[_ -]?key|secret|password|token)\b"),
        ("malware", "high", r"(?i)\b(ransomware|malware|payload dropper|keylogger)\b"),
        ("phishing", "medium", r"(?i)\b(click here|verify your account|urgent action required)\b"),
        ("pii", "medium", r"(?i)\b(?:\d{3}-\d{2}-\d{4}|\d{16})\b"),
    ]
    findings: List[SafetyFinding] = []
    for category, severity, pattern in patterns:
        for match in re.finditer(pattern, payload):
            findings.append(SafetyFinding(category=category, severity=severity, matched_text=match.group(0)))
    risk_level = "low"
    if any(f.severity == "high" for f in findings):
        risk_level = "high"
    elif findings:
        risk_level = "medium"
    return SafetyResult(
        provider=DEFAULT_PROVIDER,
        model_id=DEFAULT_MODEL_ID,
        is_safe=not findings,
        risk_level=risk_level,
        findings=findings,
        explanation="Heuristic scan completed without Vertex AI response" if not findings else "Heuristic scan detected potential unsafe content",
    )


def check_payload_safety(payload: str, project_id: Optional[str] = None, location: Optional[str] = None, model_id: str = DEFAULT_MODEL_ID) -> Dict[str, Any]:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT_ID")
    location = location or os.getenv("VERTEX_AI_LOCATION", DEFAULT_LOCATION)
    if not project_id:
        return _fallback_scan(payload).as_dict()

    client = aiplatform_v1.PredictionServiceClient()
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    response = client.predict(endpoint=endpoint, instances=[{"prompt": _build_prompt(payload)}], parameters={})
    raw_text = ""
    if response.predictions:
        first = response.predictions[0]
        if isinstance(first, dict):
            raw_text = json.dumps(first)
        else:
            raw_text = str(first)
    parsed = _extract_json(raw_text)
    findings = [SafetyFinding(**item) for item in parsed.get("findings", [])]
    return SafetyResult(
        provider=DEFAULT_PROVIDER,
        model_id=model_id,
        is_safe=bool(parsed.get("is_safe", False)),
        risk_level=str(parsed.get("risk_level", "medium")),
        findings=findings,
        explanation=parsed.get("explanation"),
    ).as_dict()


def main() -> None:
    payload = os.environ["PLAINTEXT_PAYLOAD"]
    print(json.dumps(check_payload_safety(payload), ensure_ascii=False))


if __name__ == "__main__":
    main()
