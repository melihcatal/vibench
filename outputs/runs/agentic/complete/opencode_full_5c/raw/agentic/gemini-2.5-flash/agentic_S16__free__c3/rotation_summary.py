from typing import List
from security_client import get_secrets_manager_client
from security_models import RotationStatus


def summarize_secret_rotation_status(max_results: int = 100) -> List[RotationStatus]:
    """Summarizes the rotation status of secrets in AWS Secrets Manager.

    Args:
        max_results: The maximum number of secrets to retrieve.

    Returns:
        A list of RotationStatus objects for each secret.
    """
    client = get_secrets_manager_client()
    rotation_statuses: List[RotationStatus] = []
    paginator = client.get_paginator("list_secrets")

    try:
        pages = paginator.paginate(MaxResults=max_results)
        for page in pages:
            for secret in page.get("SecretList", []):
                rotation_enabled = secret.get("RotationEnabled", False)
                rotation_rules = secret.get("RotationRules", {})

                rotation_statuses.append(
                    RotationStatus(
                        secret_name=secret.get("Name"),
                        rotation_enabled=rotation_enabled,
                        last_rotated_date=secret.get("LastRotatedDate"),
                        next_rotation_date=rotation_rules.get(
                            "AutomaticallyRotateAfterDays"
                        ),  # Simplified for example
                    )
                )
    except Exception as e:
        raise RuntimeError(f"Error summarizing secret rotation status: {e}")

    return rotation_statuses
