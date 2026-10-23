import re
from typing import Any, Dict, List, Optional

from security_models import PayloadSafetyResult, compute_payload_hash

UNSAFE_PATTERNS = [
    (r"(?i)(?:password|passwd|pwd)\s*[:=]\s*\S+", "potential_credential_pattern"),
    (r"(?i)(?:api[_-]?key|apikey)\s*[:=]\s*\S+", "potential_api_key_pattern"),
    (r"(?i)(?:secret[_-]?key|secret)\s*[:=]\s*\S+", "potential_secret_key_pattern"),
    (
        r"(?i)(?:token|auth[_-]?token|access[_-]?token)\s*[:=]\s*\S+",
        "potential_token_pattern",
    ),
    (r"(?i)(?:private[_-]?key)\s*[:=]\s*\S+", "potential_private_key_pattern"),
    (r"(?i)-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----", "pem_private_key_header"),
    (r"(?i)-----BEGIN\s+EC\s+PRIVATE\s+KEY-----", "ec_private_key_header"),
    (r"(?i)-----BEGIN\s+DSA\s+PRIVATE\s+KEY-----", "dsa_private_key_header"),
    (
        r"(?i)(?:aws[_-]?access[_-]?key[_-]?id)\s*[:=]\s*[A-Z0-9]{20}",
        "aws_access_key_pattern",
    ),
    (
        r"(?i)(?:aws[_-]?secret[_-]?access[_-]?key)\s*[:=]\s*[A-Za-z0-9/+=]{40}",
        "aws_secret_key_pattern",
    ),
    (r"(?i)(?:sk-[a-zA-Z0-9]{32,})", "openai_secret_key_pattern"),
    (r"(?i)(?:ghp_[a-zA-Z0-9]{36})", "github_personal_token_pattern"),
    (r"(?i)(?:xox[baprs]-[a-zA-Z0-9-]+)", "slack_token_pattern"),
    (r"(?i)(?:AKIA[0-9A-Z]{16})", "aws_access_key_id_pattern"),
    (
        r"(?i)(?:\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b)",
        "potential_credit_card_pattern",
    ),
    (
        r"(?i)(?:ssn|social[_-]?security)\s*[:=]\s*\d{3}[-]?\d{2}[-]?\d{4}",
        "potential_ssn_pattern",
    ),
]

SENSITIVE_KEYWORDS = [
    "password",
    "secret",
    "credential",
    "token",
    "private_key",
    "api_key",
    "access_key",
    "auth_token",
    "bearer",
]


def check_payload_safety(
    plaintext: str,
    strict_mode: bool = False,
    custom_patterns: Optional[List[str]] = None,
) -> PayloadSafetyResult:
    findings = []
    risk_level = "safe"

    for pattern, finding_name in UNSAFE_PATTERNS:
        matches = re.findall(pattern, plaintext)
        if matches:
            findings.append(finding_name)

    if custom_patterns:
        for pattern in custom_patterns:
            matches = re.findall(pattern, plaintext)
            if matches:
                findings.append(f"custom_pattern_match:{pattern}")

    for keyword in SENSITIVE_KEYWORDS:
        if re.search(rf"(?i)\b{keyword}\b", plaintext):
            if f"sensitive_keyword:{keyword}" not in findings:
                findings.append(f"sensitive_keyword:{keyword}")

    if findings:
        if len(findings) >= 3 or any(
            "private_key" in f or "credential" in f for f in findings
        ):
            risk_level = "critical"
        elif len(findings) >= 2:
            risk_level = "high"
        else:
            risk_level = "medium"

    if strict_mode and any(f.startswith("sensitive_keyword:") for f in findings):
        risk_level = max(
            risk_level,
            "medium",
            key=lambda x: {"safe": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}[
                x
            ],
        )

    payload_hash = compute_payload_hash(plaintext)

    result = PayloadSafetyResult(
        payload_hash=payload_hash,
        is_safe=(risk_level == "safe"),
        findings=findings,
        risk_level=risk_level,
    )
    return result


def scan_decrypted_payload(
    plaintext: str,
    redact: bool = False,
) -> Dict[str, Any]:
    safety_result = check_payload_safety(plaintext)

    redacted_text = plaintext
    if redact and not safety_result.is_safe:
        for pattern, _ in UNSAFE_PATTERNS:
            redacted_text = re.sub(
                pattern, "[REDACTED]", redacted_text, flags=re.IGNORECASE
            )

    return {
        "safety_check": safety_result.to_dict(),
        "redacted_text": redacted_text if redact else None,
        "original_length": len(plaintext),
        "redacted_length": len(redacted_text) if redact else None,
    }


def batch_check_payloads(
    payloads: Dict[str, str],
    strict_mode: bool = False,
) -> Dict[str, Dict[str, Any]]:
    results = {}
    for payload_id, plaintext in payloads.items():
        safety_result = check_payload_safety(plaintext, strict_mode=strict_mode)
        results[payload_id] = safety_result.to_dict()
    return results


def generate_safety_report(
    payloads: Dict[str, str],
) -> Dict[str, Any]:
    batch_results = batch_check_payloads(payloads)

    total = len(payloads)
    safe_count = sum(1 for r in batch_results.values() if r["is_safe"])
    unsafe_count = total - safe_count

    risk_distribution = {"safe": 0, "low": 0, "medium": 0, "high": 0, "critical": 0}
    all_findings = []
    for result in batch_results.values():
        risk_level = result.get("risk_level", "safe")
        risk_distribution[risk_level] = risk_distribution.get(risk_level, 0) + 1
        all_findings.extend(result.get("findings", []))

    unique_findings = list(set(all_findings))

    report = {
        "total_payloads": total,
        "safe_count": safe_count,
        "unsafe_count": unsafe_count,
        "risk_distribution": risk_distribution,
        "unique_findings": unique_findings,
        "payload_details": batch_results,
    }
    return report
