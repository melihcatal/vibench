import os
import re
import google.cloud.secretmanager as secretmanager
from typing import List, Dict, Any


def secret_label_safety(project_id: str = None) -> Dict[str, Any]:
    """
    Check secret labels and notes for unsafe text in Google Cloud Secret Manager.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = secretmanager.SecretManagerServiceClient()

    parent = f"projects/{project_id}"

    unsafe_patterns = [
        r"password\s*[:=]",  # password: or password=
        r"key\s*[:=]",  # key: or key=
        r"secret\s*[:=]",  # secret: or secret=
        r"token\s*[:=]",  # token: or token=
        r"credential\s*[:=]",  # credential: or credential=
        r"\bprod\b.*\bpass",  # prod password
        r"\blive\b.*\bkey",  # live key
        r"\broot\b",  # root access
        r"\badmin\b",  # admin access
        r"\.pem\b",  # .pem files
        r"\.key\b",  # .key files
        r"BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE",  # private key markers
    ]

    try:
        secrets = []
        unsafe_count = 0

        for secret in client.list_secrets(request={"parent": parent}):
            secret_name = secret.name.split("/")[-1]
            labels = dict(secret.labels) if secret.labels else {}
            annotations = {}

            unsafe_findings = []

            for label_key, label_value in labels.items():
                for pattern in unsafe_patterns:
                    if re.search(pattern, label_key, re.IGNORECASE):
                        unsafe_findings.append(
                            {
                                "type": "label_key",
                                "key": label_key,
                                "value": label_value,
                                "pattern": pattern,
                                "severity": "high",
                            }
                        )
                    if re.search(pattern, str(label_value), re.IGNORECASE):
                        unsafe_findings.append(
                            {
                                "type": "label_value",
                                "key": label_key,
                                "value": label_value,
                                "pattern": pattern,
                                "severity": "medium",
                            }
                        )

            if secret.annotations:
                for annotation_key, annotation_value in secret.annotations.items():
                    for pattern in unsafe_patterns:
                        if re.search(pattern, annotation_key, re.IGNORECASE):
                            unsafe_findings.append(
                                {
                                    "type": "annotation_key",
                                    "key": annotation_key,
                                    "value": annotation_value,
                                    "pattern": pattern,
                                    "severity": "high",
                                }
                            )
                        if re.search(pattern, str(annotation_value), re.IGNORECASE):
                            unsafe_findings.append(
                                {
                                    "type": "annotation_value",
                                    "key": annotation_key,
                                    "value": annotation_value,
                                    "pattern": pattern,
                                    "severity": "medium",
                                }
                            )

            for pattern in unsafe_patterns:
                if re.search(pattern, secret_name, re.IGNORECASE):
                    unsafe_findings.append(
                        {
                            "type": "secret_name",
                            "key": "name",
                            "value": secret_name,
                            "pattern": pattern,
                            "severity": "critical",
                        }
                    )

            secret_info = {
                "name": secret_name,
                "full_name": secret.name,
                "create_time": secret.create_time.isoformat(),
                "labels": labels,
                "annotations": dict(secret.annotations) if secret.annotations else {},
                "unsafe_findings": unsafe_findings,
                "is_unsafe": len(unsafe_findings) > 0,
            }

            secrets.append(secret_info)
            if secret_info["is_unsafe"]:
                unsafe_count += 1

        summary = {
            "provider": "gcp",
            "project_id": project_id,
            "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
            "total_secrets": len(secrets),
            "unsafe_secrets": unsafe_count,
            "safety_percentage": ((len(secrets) - unsafe_count) / len(secrets) * 100)
            if len(secrets) > 0
            else 100,
            "secrets": secrets,
            "unsafe_patterns": unsafe_patterns,
        }

        critical_findings = []
        high_findings = []
        medium_findings = []

        for secret in secrets:
            for finding in secret["unsafe_findings"]:
                if finding["severity"] == "critical":
                    critical_findings.append(
                        {"secret": secret["name"], "finding": finding}
                    )
                elif finding["severity"] == "high":
                    high_findings.append({"secret": secret["name"], "finding": finding})
                elif finding["severity"] == "medium":
                    medium_findings.append(
                        {"secret": secret["name"], "finding": finding}
                    )

        summary["finding_summary"] = {
            "critical": len(critical_findings),
            "high": len(high_findings),
            "medium": len(medium_findings),
            "critical_details": critical_findings[:5],
            "high_details": high_findings[:5],
        }

        return summary

    except Exception as e:
        if "PERMISSION_DENIED" in str(e):
            raise PermissionError(
                f"Permission denied accessing secrets in project {project_id}"
            ) from e
        else:
            raise RuntimeError(f"Error checking secret safety: {e}") from e
