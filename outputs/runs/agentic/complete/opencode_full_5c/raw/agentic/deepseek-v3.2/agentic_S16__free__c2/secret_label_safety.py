import boto3
import os
import re
from typing import List, Dict, Tuple
from botocore.exceptions import ClientError


def check_secret_labels_safety(secret_name: str) -> Dict[str, any]:
    """
    Check secret labels and notes for unsafe text using AWS Secrets Manager tags and description.

    Args:
        secret_name: Name of the secret

    Returns:
        Dictionary with safety check results
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Get secret metadata including tags and description
        response = client.describe_secret(SecretId=secret_name)

        description = response.get("Description", "")
        tags = {tag["Key"]: tag["Value"] for tag in response.get("Tags", [])}

        # Define unsafe patterns
        unsafe_patterns = [
            r"password\s*[:=]",  # password: or password=
            r"secret\s*[:=]",  # secret: or secret=
            r"key\s*[:=]",  # key: or key=
            r"token\s*[:=]",  # token: or token=
            r"credential\s*[:=]",  # credential: or credential=
            r"\d{3}-\d{2}-\d{4}",  # SSN-like pattern
            r"\b\d{16}\b",  # 16-digit credit card
            r"BEGIN\s+(RSA|DSA|EC)\s+PRIVATE\s+KEY",  # Private key header
            r"-----BEGIN",  # Any PEM header
            r"api[_-]?key",  # api-key, api_key, apikey
            r"aws[_-]?(access|secret)",  # aws_access, aws_secret
            r"sensitive",  # Word "sensitive"
            r"confidential",  # Word "confidential"
            r"do\s*not\s*share",  # "do not share"
            r"internal\s*use\s*only",  # "internal use only"
        ]

        # Compile patterns
        compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in unsafe_patterns
        ]

        # Check description
        description_issues = []
        for pattern in compiled_patterns:
            if pattern.search(description):
                description_issues.append(str(pattern.pattern))

        # Check tags (both keys and values)
        tag_issues = []
        for key, value in tags.items():
            tag_text = f"{key}: {value}"
            for pattern in compiled_patterns:
                if pattern.search(tag_text):
                    tag_issues.append(
                        {"tag": key, "value": value, "pattern": str(pattern.pattern)}
                    )
                    break  # Only report first match per tag

        # Get secret value to check if it contains labels in the value itself
        try:
            secret_response = client.get_secret_value(
                SecretId=secret_name, VersionStage="AWSCURRENT"
            )

            secret_text = ""
            if "SecretString" in secret_response:
                secret_text = secret_response["SecretString"]
            elif "SecretBinary" in secret_response:
                # Try to decode binary as text
                try:
                    secret_text = secret_response["SecretBinary"].decode(
                        "utf-8", errors="ignore"
                    )
                except:
                    secret_text = ""

            # Check if secret value contains label-like patterns
            value_label_issues = []
            label_patterns = [
                r'label\s*[:=]\s*["\']?([^"\'\n]+)["\']?',
                r'note\s*[:=]\s*["\']?([^"\'\n]+)["\']?',
                r'comment\s*[:=]\s*["\']?([^"\'\n]+)["\']?',
                r'description\s*[:=]\s*["\']?([^"\'\n]+)["\']?',
            ]

            for pattern in label_patterns:
                matches = re.findall(pattern, secret_text, re.IGNORECASE)
                for match in matches:
                    # Check if the extracted label contains unsafe content
                    for unsafe_pattern in compiled_patterns:
                        if unsafe_pattern.search(match):
                            value_label_issues.append(
                                {
                                    "label": match[:50] + "..."
                                    if len(match) > 50
                                    else match,
                                    "pattern": str(unsafe_pattern.pattern),
                                }
                            )
                            break

        except ClientError:
            value_label_issues = []
            secret_text = ""

        # Calculate safety score (0-100)
        total_checks = (
            len(description_issues) + len(tag_issues) + len(value_label_issues)
        )

        if total_checks == 0:
            safety_score = 100
            safety_level = "SAFE"
        elif total_checks <= 2:
            safety_score = 70
            safety_level = "LOW_RISK"
        elif total_checks <= 5:
            safety_score = 40
            safety_level = "MEDIUM_RISK"
        else:
            safety_score = 10
            safety_level = "HIGH_RISK"

        result = {
            "secret_name": secret_name,
            "description": description,
            "tags": tags,
            "description_issues": description_issues,
            "tag_issues": tag_issues,
            "value_label_issues": value_label_issues,
            "total_issues": total_checks,
            "safety_score": safety_score,
            "safety_level": safety_level,
            "recommendations": [],
        }

        # Generate recommendations
        if description_issues:
            result["recommendations"].append(
                "Remove sensitive keywords from secret description"
            )

        if tag_issues:
            result["recommendations"].append(
                "Review and clean up tags that contain sensitive information"
            )

        if value_label_issues:
            result["recommendations"].append(
                "Remove inline labels/notes from secret value that contain sensitive terms"
            )

        if total_checks > 0:
            result["recommendations"].append(
                "Consider using generic labels like 'prod', 'staging', 'service-x' instead of descriptive labels"
            )

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise Exception(f"Secret '{secret_name}' not found in AWS Secrets Manager")
        else:
            raise Exception(f"Failed to check secret labels: {e}")


def get_safety_report(secret_name: str) -> str:
    """
    Generate a human-readable safety report.

    Args:
        secret_name: Name of the secret

    Returns:
        Formatted safety report
    """
    safety_check = check_secret_labels_safety(secret_name)

    lines = []
    lines.append(f"Safety Check Report for: {safety_check['secret_name']}")
    lines.append(f"Safety Level: {safety_check['safety_level']}")
    lines.append(f"Safety Score: {safety_check['safety_score']}/100")
    lines.append(f"Total Issues Found: {safety_check['total_issues']}")
    lines.append("")

    if safety_check["description_issues"]:
        lines.append("⚠️  Issues in Description:")
        for issue in safety_check["description_issues"]:
            lines.append(f"  - Matches pattern: {issue}")

    if safety_check["tag_issues"]:
        lines.append("⚠️  Issues in Tags:")
        for issue in safety_check["tag_issues"]:
            lines.append(f"  - Tag '{issue['tag']}': {issue['value']}")
            lines.append(f"    Matches pattern: {issue['pattern']}")

    if safety_check["value_label_issues"]:
        lines.append("⚠️  Issues in Secret Value Labels:")
        for issue in safety_check["value_label_issues"]:
            lines.append(f"  - Label: {issue['label']}")
            lines.append(f"    Matches pattern: {issue['pattern']}")

    if safety_check["recommendations"]:
        lines.append("")
        lines.append("📋 Recommendations:")
        for rec in safety_check["recommendations"]:
            lines.append(f"  • {rec}")

    return "\n".join(lines)


if __name__ == "__main__":
    report = get_safety_report("prod/api-key")
    print(report)
