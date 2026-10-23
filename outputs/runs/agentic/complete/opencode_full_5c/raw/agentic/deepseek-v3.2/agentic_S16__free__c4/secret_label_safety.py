import os
import re
from typing import List, Dict, Any, Tuple
from google.cloud import secretmanager


def check_secret_label_safety(project_id: str, secret_id: str = None) -> Dict[str, Any]:
    """Check secret labels and notes for unsafe text in Google Cloud Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()

    unsafe_patterns = [
        r"password\s*[:=]\s*\S+",  # password: value
        r"key\s*[:=]\s*\S+",  # key: value
        r"secret\s*[:=]\s*\S+",  # secret: value
        r"token\s*[:=]\s*\S+",  # token: value
        r"credential\s*[:=]\s*\S+",  # credential: value
        r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # phone numbers
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # email addresses
        r"\b\d{16}\b",  # credit card numbers
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    ]

    findings = {"unsafe_labels": [], "unsafe_notes": [], "warnings": [], "safe": True}

    try:
        if secret_id:
            secret_name = f"projects/{project_id}/secrets/{secret_id}"
            secret = client.get_secret(request={"name": secret_name})
            secrets_to_check = [(secret_id, secret)]
        else:
            secrets_to_check = []
            parent = f"projects/{project_id}"
            for secret in client.list_secrets(request={"parent": parent}):
                secret_id = secret.name.split("/")[-1]
                secrets_to_check.append((secret_id, secret))

        for secret_id, secret in secrets_to_check:
            # Check labels
            if secret.labels:
                for label_key, label_value in secret.labels.items():
                    for pattern in unsafe_patterns:
                        if re.search(pattern, label_key, re.IGNORECASE) or re.search(
                            pattern, label_value, re.IGNORECASE
                        ):
                            findings["unsafe_labels"].append(
                                {
                                    "secret_id": secret_id,
                                    "label_key": label_key,
                                    "label_value": label_value[:50] + "..."
                                    if len(label_value) > 50
                                    else label_value,
                                    "pattern_matched": pattern,
                                }
                            )
                            findings["safe"] = False

            # Check notes/annotations (in metadata)
            if hasattr(secret, "annotations") and secret.annotations:
                for annotation_key, annotation_value in secret.annotations.items():
                    for pattern in unsafe_patterns:
                        if re.search(
                            pattern, annotation_key, re.IGNORECASE
                        ) or re.search(pattern, annotation_value, re.IGNORECASE):
                            findings["unsafe_notes"].append(
                                {
                                    "secret_id": secret_id,
                                    "annotation_key": annotation_key,
                                    "annotation_value": annotation_value[:50] + "..."
                                    if len(annotation_value) > 50
                                    else annotation_value,
                                    "pattern_matched": pattern,
                                }
                            )
                            findings["safe"] = False

            # Check for common warning patterns
            warning_patterns = [
                (r"test|demo|example", "Test/demo label"),
                (r"temp|temporary", "Temporary label"),
                (r"old|deprecated|legacy", "Outdated label"),
                (r"dev|development", "Development environment label"),
            ]

            if secret.labels:
                for label_key, label_value in secret.labels.items():
                    for pattern, warning in warning_patterns:
                        if re.search(pattern, label_key, re.IGNORECASE) or re.search(
                            pattern, label_value, re.IGNORECASE
                        ):
                            findings["warnings"].append(
                                {
                                    "secret_id": secret_id,
                                    "label_key": label_key,
                                    "label_value": label_value[:50] + "..."
                                    if len(label_value) > 50
                                    else label_value,
                                    "warning": warning,
                                }
                            )

    except Exception as e:
        if "NOT_FOUND" in str(e):
            raise ValueError(f"Secret {secret_id} not found in project {project_id}")
        elif "PERMISSION_DENIED" in str(e):
            raise PermissionError(f"Permission denied accessing project {project_id}")
        else:
            raise RuntimeError(f"Error accessing Google Cloud Secret Manager: {e}")

    return findings


def generate_safety_report(findings: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a safety report from findings."""
    report = {
        "scan_timestamp": os.environ.get("SCAN_TIMESTAMP", "unknown"),
        "total_unsafe_labels": len(findings["unsafe_labels"]),
        "total_unsafe_notes": len(findings["unsafe_notes"]),
        "total_warnings": len(findings["warnings"]),
        "overall_safe": findings["safe"],
        "details": findings,
    }

    if not findings["safe"]:
        report["recommendations"] = [
            "Remove sensitive information from labels and annotations",
            "Use generic labels without actual values",
            "Consider moving sensitive data to the secret value itself",
            "Review and clean up test/demo labels in production",
        ]

    return report
