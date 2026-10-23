from security_client import get_secrets_manager_client


def rotation_summary(payload, config=None):
    client = get_secrets_manager_client(config)
    response = client.describe_secret(SecretId=payload["secret_id"])
    rotation_enabled = response.get("RotationEnabled", False)
    return {"secret_id": payload["secret_id"], "rotation_enabled": rotation_enabled, "last_changed_date": response.get("LastChangedDate"), "rotation_rules": response.get("RotationRules", {})}
