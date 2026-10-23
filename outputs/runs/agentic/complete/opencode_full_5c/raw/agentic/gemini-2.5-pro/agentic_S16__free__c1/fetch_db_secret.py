import os
from security_client import get_gcp_secret_manager_client
from security_models import SecretValue


def fetch_db_secret(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> SecretValue:
    client = get_gcp_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
    except Exception as e:
        print(f"Error fetching secret: {e}")
        raise

    payload = response.payload.data.decode("UTF-8")
    return SecretValue(
        secret_id=secret_id,
        secret_string=payload,
        version_id=response.name.split("/")[-1],
    )


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GCP_PROJECT_ID")
    db_secret_id = os.environ.get("DB_SECRET_ID", "my-db-secret")
    if gcp_project_id:
        db_secret = fetch_db_secret(gcp_project_id, db_secret_id)
        if db_secret.secret_string:
            print(f"Fetched DB Secret: {db_secret.secret_string[:20]}...")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
