import os
import re
from security_client import create_secrets_manager_client, describe_secret
from security_models import SecretLabel, LabelSafetyReport, build_aws_secret_request


UNSAFE_PATTERNS = [
    (r"(?i)(password|passwd|pwd)\s*[=:]\s*\S+", "contains embedded password"),
    (r"(?i)(api[_-]?key|apikey)\s*[=:]\s*[A-Za-z0-9]{16,}", "contains exposed API key"),
    (
        r"(?i)(secret|token)\s*[=:]\s*[A-Za-z0-9+/=]{20,}",
        "contains exposed secret or token",
    ),
    (
        r"(?i)(aws[_-]?access[_-]?key[_-]?id)\s*[=:]\s*AKIA[0-9A-Z]{16}",
        "contains AWS access key",
    ),
    (
        r"(?i)(private[_-]?key|BEGIN\s+(RSA\s+)?PRIVATE\s+KEY)",
        "contains private key reference",
    ),
    (
        r"(?i)(connection[_-]?string|conn[_-]?str)\s*[=:]\s*\S+://\S+:\S+@",
        "contains connection string with credentials",
    ),
]

UNSAFE_KEYWORDS = [
    "hardcoded",
    "plaintext",
    "do not rotate",
    "skip rotation",
    "bypass auth",
    "disable encryption",
    "test credential",
    "temporary bypass",
]


def check_label_safety(secret_id: str, region: str = None) -> LabelSafetyReport:
    request = build_aws_secret_request(secret_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = describe_secret(client, request.secret_id)
    tags = aws_response.get("Tags", [])
    labels = [SecretLabel(key=t.get("Key", ""), value=t.get("Value", "")) for t in tags]
    report = evaluate_label_safety(secret_id, labels)
    return report


def evaluate_label_safety(secret_id: str, labels: list) -> LabelSafetyReport:
    unsafe_labels = []
    overall_safe = True

    for label in labels:
        label.is_safe, label.flagged_reasons = _check_single_label(label)
        if not label.is_safe:
            overall_safe = False
            unsafe_labels.append(
                {
                    "key": label.key,
                    "value": label.value,
                    "reasons": label.flagged_reasons,
                }
            )

    report = LabelSafetyReport(
        secret_id=secret_id,
        labels=[{"key": l.key, "value": l.value, "is_safe": l.is_safe} for l in labels],
        overall_safe=overall_safe,
        unsafe_labels=unsafe_labels,
        checked_at=str(
            __import__("datetime")
            .datetime.now(__import__("datetime").timezone.utc)
            .isoformat()
        ),
    )
    return report


def _check_single_label(label: SecretLabel) -> tuple:
    reasons = []
    combined_text = f"{label.key} {label.value}"

    for pattern, description in UNSAFE_PATTERNS:
        if re.search(pattern, combined_text):
            reasons.append(description)

    for keyword in UNSAFE_KEYWORDS:
        if keyword.lower() in combined_text.lower():
            reasons.append(f"contains unsafe keyword: '{keyword}'")

    is_safe = len(reasons) == 0
    return is_safe, reasons


def check_secret_value_safety(secret_id: str, region: str = None) -> dict:
    from security_models import normalize_secret_payload
    from security_client import get_secret_value

    request = build_aws_secret_request(secret_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(client, request.secret_id)
    payload = normalize_secret_payload(aws_response.get("SecretString", ""))

    value_labels = []
    for key, value in payload.items():
        value_labels.append(SecretLabel(key=key, value=str(value)))

    report = evaluate_label_safety(secret_id, value_labels)
    return report.to_dict()


if __name__ == "__main__":
    target_secret_id = os.environ.get("LABEL_CHECK_SECRET_ID", "prod/api/payment-key")
    result = check_label_safety(target_secret_id)
    print(result.to_dict())
