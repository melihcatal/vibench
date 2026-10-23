from security_client import secrets_manager_client


def rotation_summary(payload, config=None):
    client = secrets_manager_client(config)
    response = client.describe_secret(SecretId=payload["secret_id"])
    return {
        "rotation_enabled": response.get("RotationEnabled", False),
        "next_rotation_date": response.get("NextRotationDate"),
        "last_changed_date": response.get("LastChangedDate"),
    }
