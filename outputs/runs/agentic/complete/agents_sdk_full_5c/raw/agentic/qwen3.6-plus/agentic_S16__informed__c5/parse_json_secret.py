"""Retrieve and parse a JSON-formatted secret from Google Cloud Secret Manager."""

import json
import os
from google.cloud import secretmanager_v1 as secretmanager


def parse_json_secret(
    secret_id: str,
    project_id: str | None = None,
    version: str = "latest",
) -> dict:
    """Retrieve and parse a JSON secret from Google Cloud Secret Manager.

    Args:
        secret_id: The short name of the secret (not the full resource path).
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
        version: Secret version to retrieve, defaults to 'latest'.

    Returns:
        The parsed JSON object as a dictionary.

    Raises:
        ValueError: If the secret payload is not valid JSON or project ID is missing.
        Exception: If the secret cannot be accessed.
    """
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "project_id or GOOGLE_CLOUD_PROJECT environment variable is required"
        )

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"

    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Secret '{secret_id}' does not contain valid JSON"
        ) from exc


if __name__ == "__main__":
    sid = os.environ.get("SECRET_ID", "app-config")
    parsed = parse_json_secret(sid)
    print(json.dumps(parsed, indent=2))
