import os
import re
from typing import List, Dict, Tuple
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound, PermissionDenied


class SecretLabelSafetyChecker:
    """Check secret labels and notes for unsafe text in Google Cloud Secret Manager."""

    # Unsafe patterns to check for
    UNSAFE_PATTERNS = {
        "password_in_label": r"(?i)password|pwd|pass|credential|secret",
        "key_in_label": r"(?i)api[_-]?key|private[_-]?key|access[_-]?key",
        "token_in_label": r"(?i)token|auth|bearer",
        "connection_string": r"(?i)connection[_-]?string|conn[_-]?str|dsn",
        "url_with_credentials": r"://[^:]+:[^@]+@",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "email_address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "ssh_private_key": r"-----BEGIN (?:RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
        "jwt_token": r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$",
    }

    def __init__(self, project_id: str = None):
        """
        Initialize checker with Google Cloud project.

        Args:
            project_id: GCP project ID (defaults to environment variable)
        """
        if project_id is None:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def check_secret_labels(self, secret_id: str) -> Dict[str, any]:
        """
        Check labels of a specific secret for unsafe content.

        Args:
            secret_id: ID of the secret to check

        Returns:
            Dictionary with safety check results
        """
        secret_name = f"projects/{self.project_id}/secrets/{secret_id}"

        try:
            # Get secret metadata including labels
            secret = self.client.get_secret(request={"name": secret_name})
            labels = dict(secret.labels) if secret.labels else {}

            # Check labels for unsafe patterns
            label_issues = []
            for label_key, label_value in labels.items():
                issues = self._check_text_for_unsafe_patterns(
                    f"{label_key}: {label_value}"
                )
                if issues:
                    label_issues.append(
                        {"label": label_key, "value": label_value, "issues": issues}
                    )

            # Get secret versions to check notes
            versions = list(
                self.client.list_secret_versions(request={"parent": secret_name})
            )

            # Check version notes
            version_issues = []
            for version in versions:
                if version.state.name == "ENABLED" and version.annotations:
                    annotations = dict(version.annotations)
                    for ann_key, ann_value in annotations.items():
                        issues = self._check_text_for_unsafe_patterns(
                            f"{ann_key}: {ann_value}"
                        )
                        if issues:
                            version_issues.append(
                                {
                                    "version": version.name.split("/")[-1],
                                    "annotation": ann_key,
                                    "value": ann_value,
                                    "issues": issues,
                                }
                            )

            # Overall safety assessment
            total_issues = len(label_issues) + len(version_issues)
            safety_level = "safe" if total_issues == 0 else "unsafe"

            if total_issues > 0:
                if any(
                    any("high" in issue["severity"] for issue in item["issues"])
                    for item in label_issues + version_issues
                ):
                    safety_level = "critical"
                elif total_issues > 3:
                    safety_level = "high_risk"

            return {
                "secret_id": secret_id,
                "project_id": self.project_id,
                "safety_level": safety_level,
                "label_issues": label_issues,
                "version_issues": version_issues,
                "total_issues": total_issues,
                "has_labels": bool(labels),
                "label_count": len(labels),
            }

        except NotFound:
            raise ValueError(
                f"Secret {secret_id} not found in project {self.project_id}"
            )
        except PermissionDenied:
            raise PermissionError(f"Permission denied to access secret {secret_id}")
        except Exception as e:
            raise RuntimeError(f"Error checking secret labels: {e}")

    def _check_text_for_unsafe_patterns(self, text: str) -> List[Dict[str, str]]:
        """
        Check text for unsafe patterns.

        Args:
            text: Text to check

        Returns:
            List of issues found
        """
        issues = []

        for pattern_name, pattern in self.UNSAFE_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                # Determine severity
                if pattern_name in [
                    "password_in_label",
                    "key_in_label",
                    "token_in_label",
                ]:
                    severity = "high"
                elif pattern_name in ["connection_string", "url_with_credentials"]:
                    severity = "critical"
                elif pattern_name in ["ssh_private_key", "jwt_token"]:
                    severity = "critical"
                else:
                    severity = "medium"

                issues.append(
                    {
                        "pattern": pattern_name,
                        "matches": matches,
                        "severity": severity,
                        "description": f"Found {pattern_name.replace('_', ' ')} in text",
                    }
                )

        return issues

    def check_all_secrets_in_project(self) -> Dict[str, any]:
        """
        Check all secrets in the project for label safety.

        Returns:
            Summary of safety checks across all secrets
        """
        parent = f"projects/{self.project_id}"

        try:
            secrets = list(self.client.list_secrets(request={"parent": parent}))

            results = {
                "project_id": self.project_id,
                "total_secrets": len(secrets),
                "unsafe_secrets": 0,
                "critical_secrets": 0,
                "secrets_checked": [],
            }

            for secret in secrets:
                secret_id = secret.name.split("/")[-1]
                try:
                    check_result = self.check_secret_labels(secret_id)
                    results["secrets_checked"].append(check_result)

                    if check_result["safety_level"] == "critical":
                        results["critical_secrets"] += 1
                        results["unsafe_secrets"] += 1
                    elif check_result["safety_level"] in ["unsafe", "high_risk"]:
                        results["unsafe_secrets"] += 1

                except Exception as e:
                    # Skip secrets we can't access
                    continue

            return results

        except Exception as e:
            raise RuntimeError(f"Error checking all secrets: {e}")
