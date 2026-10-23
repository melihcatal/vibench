from security_models import SecretResponse
import re


def secret_label_safety(secret_response: SecretResponse) -> Dict[str, Any]:
    unsafe_patterns = [
        r"password",
        r"secret",
        r"key",
        r"token",
        r"credential",
        r"admin",
        r"root",
    ]

    findings = {"unsafe_labels": [], "unsafe_notes": []}

    for label_key, label_value in secret_response.labels.items():
        for pattern in unsafe_patterns:
            if re.search(pattern, label_key, re.IGNORECASE) or re.search(
                pattern, label_value, re.IGNORECASE
            ):
                findings["unsafe_labels"].append(
                    {"label": label_key, "value": label_value, "pattern": pattern}
                )

    if secret_response.notes:
        for pattern in unsafe_patterns:
            if re.search(pattern, secret_response.notes, re.IGNORECASE):
                findings["unsafe_notes"].append(
                    {"text": secret_response.notes, "pattern": pattern}
                )

    return {
        "is_safe": not (findings["unsafe_labels"] or findings["unsafe_notes"]),
        "findings": findings,
        "provider": "google-cloud-secret-manager",
    }
