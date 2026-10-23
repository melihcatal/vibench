import os
from typing import Optional

from google.cloud import secretmanager


def _client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def read_secret_version(project_id: str, secret_id: str, version: Optional[str] = None, stage: Optional[str] = None) -> str:
    client = _client()
    if version and stage:
        raise ValueError("Specify either version or stage, not both")
    if version:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    elif stage:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{stage}"
    else:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    secret_id = os.environ["SECRET_ID"]
    version = os.environ.get("SECRET_VERSION")
    stage = os.environ.get("SECRET_STAGE")
    print(read_secret_version(project_id, secret_id, version=version, stage=stage))


if __name__ == "__main__":
    main()
