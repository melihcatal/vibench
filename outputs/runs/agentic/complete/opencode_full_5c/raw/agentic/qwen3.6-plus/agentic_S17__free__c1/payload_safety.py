import os
import json
from typing import List, Dict, Any, Optional
from security_models import PayloadSafetyResult
from security_client import get_comprehend_client, load_aws_config


SENSITIVE_PATTERNS = [
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "private_key",
    "credential",
    "ssn",
    "social security",
    "credit card",
    "cvv",
    "pin",
]

PII_LABELS = [
    "NAME",
    "ADDRESS",
    "EMAIL",
    "PHONE",
    "CREDIT_DEBIT_NUMBER",
    "CREDIT_DEBIT_CVV",
    "CREDIT_DEBIT_EXPIRY",
    "PIN",
    "SSN",
    "BANK_ACCOUNT_NUMBER",
    "BANK_ROUTING",
    "PASSWORD",
    "USERNAME",
]


def check_payload_safety(
    text: str,
    detect_pii: bool = True,
    detect_sensitive_patterns: bool = True,
    min_confidence: float = 0.7,
) -> PayloadSafetyResult:
    findings: List[Dict[str, Any]] = []
    is_safe = True

    if detect_sensitive_patterns:
        text_lower = text.lower()
        for pattern in SENSITIVE_PATTERNS:
            if pattern in text_lower:
                is_safe = False
                findings.append(
                    {
                        "type": "sensitive_pattern",
                        "pattern": pattern,
                        "confidence": 1.0,
                        "message": f"Sensitive pattern detected: {pattern}",
                    }
                )

    if detect_pii:
        config = load_aws_config()
        comprehend_client = get_comprehend_client(config)

        try:
            pii_response = comprehend_client.detect_pii_entities(
                Text=text,
                LanguageCode="en",
            )

            for entity in pii_response.get("Entities", []):
                entity_type = entity.get("Type", "")
                score = entity.get("Score", 0.0)
                if score >= min_confidence and entity_type in PII_LABELS:
                    is_safe = False
                    findings.append(
                        {
                            "type": "pii_entity",
                            "entity_type": entity_type,
                            "confidence": score,
                            "begin_offset": entity.get("BeginOffset"),
                            "end_offset": entity.get("EndOffset"),
                            "message": f"PII entity detected: {entity_type} (confidence: {score:.2f})",
                        }
                    )
        except Exception as e:
            findings.append(
                {
                    "type": "error",
                    "message": f"AWS Comprehend PII detection failed: {str(e)}",
                    "confidence": 0.0,
                }
            )

    max_confidence = max([f.get("confidence", 0.0) for f in findings], default=0.0)

    return PayloadSafetyResult(
        text=text,
        is_safe=is_safe,
        findings=findings,
        confidence=max_confidence,
    )


def format_safety_report(result: PayloadSafetyResult) -> str:
    lines = [
        f"Payload Safety Check (via AWS Comprehend)",
        f"Safe: {result.is_safe}",
        f"Max Confidence: {result.confidence:.2f}",
        f"Findings ({len(result.findings)}):",
    ]
    for finding in result.findings:
        lines.append(f"  - [{finding['type']}] {finding.get('message', 'N/A')}")
    return "\n".join(lines)


if __name__ == "__main__":
    result = check_payload_safety("My SSN is 123-45-6789 and password is secret123")
    print(format_safety_report(result))
