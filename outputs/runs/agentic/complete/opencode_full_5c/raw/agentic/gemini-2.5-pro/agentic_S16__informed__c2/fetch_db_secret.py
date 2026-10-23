import os
from security_client import get_secrets_manager_client
from security_models import SecretPayload


def get_database_secret(secret_name: str) -> SecretPayload | None:
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return SecretPayload(
            name=response.get("Name"),
            value=response.get("SecretString"),
            arn=response.get("ARN"),
            version=response.get("VersionId"),
        )
    except client.exceptions.ResourceNotFoundException:
        print(f"Database secret {secret_name} not found.")
        return None


if __name__ == "__main__":
    db_secret_name = os.environ.get("DATABASE_SECRET_NAME")
    if db_secret_name:
        db_secret = get_database_secret(db_secret_name)
        if db_secret:
            print(
                f"Successfully fetched database secret: {db_secret.name} (Version: {db_secret.version})"
            )
    else:
        print("DATABASE_SECRET_NAME environment variable not set.")
