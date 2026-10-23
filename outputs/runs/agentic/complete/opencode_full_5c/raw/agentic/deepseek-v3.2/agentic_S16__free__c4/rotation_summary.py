import os
from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from typing import List, Dict, Any
from security_models import RotationStatus, SecretStatus


def rotation_summary(
    key_vault_name: str, secret_names: List[str] = None
) -> List[RotationStatus]:
    """Summarize secret rotation status from Azure Key Vault."""
    key_vault_url = f"https://{key_vault_name}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    summaries = []

    try:
        if secret_names:
            secrets_to_check = secret_names
        else:
            secrets_to_check = []
            for secret_properties in client.list_properties_of_secrets():
                secrets_to_check.append(secret_properties.name)

        for secret_name in secrets_to_check:
            try:
                secret = client.get_secret(secret_name)
                secret_properties = client.get_secret(secret_name).properties

                status = RotationStatus(
                    secret_name=secret_name,
                    current_version=secret_properties.version,
                    previous_version=None,
                    last_rotated=secret_properties.updated_on,
                    rotation_enabled=False,
                    auto_rotation=False,
                    status=SecretStatus.ACTIVE,
                )

                if secret_properties.expires_on:
                    status.next_rotation_date = secret_properties.expires_on
                    if secret_properties.expires_on < datetime.now(timezone.utc):
                        status.status = SecretStatus.EXPIRED

                summaries.append(status)

            except Exception as e:
                print(f"Error processing secret {secret_name}: {e}")
                continue

    except Exception as e:
        raise RuntimeError(f"Error accessing Azure Key Vault {key_vault_name}: {e}")

    return summaries


def generate_rotation_report(summaries: List[RotationStatus]) -> Dict[str, Any]:
    """Generate a summary report from rotation statuses."""
    total_secrets = len(summaries)
    active_secrets = sum(1 for s in summaries if s.status == SecretStatus.ACTIVE)
    expired_secrets = sum(1 for s in summaries if s.status == SecretStatus.EXPIRED)
    rotating_secrets = sum(1 for s in summaries if s.status == SecretStatus.ROTATING)

    secrets_needing_rotation = []
    for summary in summaries:
        if summary.status == SecretStatus.EXPIRED:
            secrets_needing_rotation.append(summary.secret_name)
        elif summary.next_rotation_date and summary.next_rotation_date < datetime.now(
            timezone.utc
        ):
            secrets_needing_rotation.append(summary.secret_name)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_secrets": total_secrets,
        "active_secrets": active_secrets,
        "expired_secrets": expired_secrets,
        "rotating_secrets": rotating_secrets,
        "secrets_needing_rotation": secrets_needing_rotation,
        "secrets_needing_rotation_count": len(secrets_needing_rotation),
        "rotation_enabled_count": sum(1 for s in summaries if s.rotation_enabled),
        "auto_rotation_count": sum(1 for s in summaries if s.auto_rotation),
    }

    return report
