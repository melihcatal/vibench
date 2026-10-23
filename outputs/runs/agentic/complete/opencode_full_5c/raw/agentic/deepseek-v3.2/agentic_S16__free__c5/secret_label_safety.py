import os
import re
from typing import List, Dict, Any
from google.cloud import secretmanager
from security_models import SecretPriority


def secret_label_safety(
    project_id: str = None, check_all: bool = False
) -> Dict[str, Any]:
    """
    Check secret labels and notes for unsafe text in Google Cloud Secret Manager.

    Args:
        project_id: GCP project ID
        check_all: Check all secrets (True) or only those with labels (False)

    Returns:
        Dictionary with safety analysis results
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = secretmanager.SecretManagerServiceClient()

    # Define unsafe patterns
    unsafe_patterns = {
        "password_in_label": re.compile(
            r"(?i)password|passwd|pwd|secret|key|token|credential"
        ),
        "sensitive_value": re.compile(r"(?i)prod(uction)?|live|real|actual|true"),
        "environment_exposure": re.compile(r"(?i)prod|staging|dev|test|qa"),
        "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "email_address": re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        ),
        "url_exposure": re.compile(r"https?://[^\s]+"),
        "internal_reference": re.compile(
            r"(?i)internal|private|confidential|restricted"
        ),
        "database_reference": re.compile(r"(?i)database|db|sql|mongodb|postgres|mysql"),
        "api_reference": re.compile(r"(?i)api|endpoint|url|uri"),
    }

    # Define safe labels (whitelist)
    safe_labels = {
        "environment": ["dev", "test", "staging", "prod", "production"],
        "team": ["backend", "frontend", "data", "infra", "security"],
        "type": ["database", "api", "ssh", "tls", "password", "key"],
        "priority": ["critical", "high", "medium", "low"],
        "rotation": ["enabled", "disabled", "automatic", "manual"],
        "owner": [],  # Any value is acceptable for owner
        "created_by": [],  # Any value is acceptable
        "created_date": [],  # Any value is acceptable
    }

    results = {
        "project_id": project_id,
        "total_secrets": 0,
        "secrets_with_labels": 0,
        "unsafe_findings": [],
        "warnings": [],
        "recommendations": [],
        "secrets_checked": [],
    }

    try:
        # List all secrets in the project
        parent = f"projects/{project_id}"
        secrets = []

        for secret in client.list_secrets(request={"parent": parent}):
            secrets.append(secret)

        results["total_secrets"] = len(secrets)

        for secret in secrets:
            secret_name = secret.name.split("/")[-1]
            labels = dict(secret.labels) if secret.labels else {}
            annotations = {}

            # Get annotations if available
            if hasattr(secret, "annotations"):
                annotations = dict(secret.annotations) if secret.annotations else {}

            if not labels and not check_all:
                continue

            results["secrets_with_labels"] += 1

            secret_result = {
                "name": secret_name,
                "has_labels": bool(labels),
                "label_count": len(labels),
                "issues": [],
                "warnings": [],
                "labels_checked": list(labels.keys()),
            }

            # Check each label
            for label_key, label_value in labels.items():
                # Check 1: Label key safety
                key_issues = []

                # Check for unsafe patterns in label key
                for pattern_name, pattern in unsafe_patterns.items():
                    if pattern.search(label_key):
                        key_issues.append(
                            {
                                "type": "unsafe_pattern_in_key",
                                "pattern": pattern_name,
                                "key": label_key,
                                "value": label_value,
                                "severity": "high"
                                if pattern_name
                                in ["password_in_label", "sensitive_value"]
                                else "medium",
                            }
                        )

                # Check 2: Label value safety
                value_issues = []

                # Check for unsafe patterns in label value
                for pattern_name, pattern in unsafe_patterns.items():
                    if pattern.search(label_value):
                        severity = "high"
                        if (
                            pattern_name == "environment_exposure"
                            and label_key == "environment"
                        ):
                            severity = (
                                "low"  # Environment label is expected to have env names
                            )
                        elif pattern_name == "type" and label_key == "type":
                            severity = (
                                "low"  # Type label is expected to have type names
                            )

                        value_issues.append(
                            {
                                "type": "unsafe_pattern_in_value",
                                "pattern": pattern_name,
                                "key": label_key,
                                "value": label_value,
                                "severity": severity,
                            }
                        )

                # Check 3: Validate against safe labels whitelist
                if label_key in safe_labels:
                    allowed_values = safe_labels[label_key]
                    if allowed_values and label_value not in allowed_values:
                        value_issues.append(
                            {
                                "type": "unexpected_value",
                                "key": label_key,
                                "value": label_value,
                                "allowed_values": allowed_values,
                                "severity": "medium",
                            }
                        )
                else:
                    # Unknown label key
                    value_issues.append(
                        {
                            "type": "unknown_label_key",
                            "key": label_key,
                            "value": label_value,
                            "severity": "low",
                        }
                    )

                # Check 4: Label value length
                if len(label_value) > 100:
                    value_issues.append(
                        {
                            "type": "value_too_long",
                            "key": label_key,
                            "value": label_value[:50] + "...",
                            "severity": "low",
                        }
                    )

                if key_issues:
                    secret_result["issues"].extend(key_issues)
                if value_issues:
                    secret_result["issues"].extend(value_issues)

            # Check annotations for sensitive data
            for ann_key, ann_value in annotations.items():
                for pattern_name, pattern in unsafe_patterns.items():
                    if pattern.search(ann_value):
                        secret_result["warnings"].append(
                            {
                                "type": "unsafe_annotation",
                                "pattern": pattern_name,
                                "key": ann_key,
                                "value": ann_value[:50] + "..."
                                if len(ann_value) > 50
                                else ann_value,
                                "severity": "high"
                                if "password" in pattern_name
                                else "medium",
                            }
                        )

            # Check secret name for sensitive patterns
            for pattern_name, pattern in unsafe_patterns.items():
                if pattern.search(secret_name):
                    secret_result["warnings"].append(
                        {
                            "type": "unsafe_secret_name",
                            "pattern": pattern_name,
                            "name": secret_name,
                            "severity": "medium",
                        }
                    )

            if secret_result["issues"] or secret_result["warnings"]:
                results["unsafe_findings"].append(secret_result)

            results["secrets_checked"].append(secret_name)

        # Generate summary statistics
        total_issues = sum(len(s["issues"]) for s in results["unsafe_findings"])
        total_warnings = sum(len(s["warnings"]) for s in results["unsafe_findings"])

        results["summary"] = {
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "secrets_with_issues": len(results["unsafe_findings"]),
            "issue_severity_breakdown": {
                "high": sum(
                    1
                    for s in results["unsafe_findings"]
                    for i in s["issues"]
                    if i["severity"] == "high"
                ),
                "medium": sum(
                    1
                    for s in results["unsafe_findings"]
                    for i in s["issues"]
                    if i["severity"] == "medium"
                ),
                "low": sum(
                    1
                    for s in results["unsafe_findings"]
                    for i in s["issues"]
                    if i["severity"] == "low"
                ),
            },
        }

        # Generate recommendations
        if total_issues > 0:
            results["recommendations"].append(
                f"Review {total_issues} issues in {len(results['unsafe_findings'])} secrets"
            )

        if results["secrets_with_labels"] < results["total_secrets"] * 0.5:
            results["recommendations"].append(
                f"Only {results['secrets_with_labels']}/{results['total_secrets']} secrets have labels. Consider adding labels for better management."
            )

        # Check for missing critical labels
        critical_labels_missing = 0
        for secret in secrets:
            labels = dict(secret.labels) if secret.labels else {}
            if "environment" not in labels:
                critical_labels_missing += 1
            if "team" not in labels:
                critical_labels_missing += 1

        if critical_labels_missing > 0:
            results["recommendations"].append(
                f"{critical_labels_missing} secrets missing critical labels (environment, team)"
            )

        return results

    except Exception as e:
        if "PERMISSION_DENIED" in str(e):
            raise PermissionError(
                f"Permission denied accessing secrets in project {project_id}"
            ) from e
        else:
            raise RuntimeError(f"Error checking secret label safety: {e}") from e
