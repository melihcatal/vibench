import boto3
from botocore.exceptions import ClientError
import re
import os


def check_secret_label_safety(
    secret_name: str, region_name: str = "us-east-1"
) -> Dict[str, Any]:
    """
    Checks secret labels and notes in AWS Secrets Manager for unsafe text.

    Args:
        secret_name: Name of the secret to check.
        region_name: AWS region where the secret is stored.

    Returns:
        A dictionary containing safety status and unsafe patterns found.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    unsafe_patterns = [
        r"password",
        r"secret",
        r"key",
        r"token",
        r"credential",
        r"admin",
        r"root",
    ]

    try:
        response = client.describe_secret(SecretId=secret_name)
        labels = response.get("Tags", [])
        description = response.get("Description", "")

        unsafe_findings = []

        # Check description
        for pattern in unsafe_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                unsafe_findings.append(
                    f"Description contains unsafe pattern: {pattern}"
                )

        # Check tags
        for tag in labels:
            for pattern in unsafe_patterns:
                if re.search(pattern, tag["Key"], re.IGNORECASE) or re.search(
                    pattern, tag["Value"], re.IGNORECASE
                ):
                    unsafe_findings.append(f"Tag contains unsafe pattern: {pattern}")

        return {
            "secret_name": secret_name,
            "is_safe": len(unsafe_findings) == 0,
            "unsafe_findings": unsafe_findings,
        }
    except ClientError as e:
        raise Exception(f"Failed to check secret labels: {e}")
