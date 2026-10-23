"""Read a specific secret version or staged value from Doppler Secrets."""

import os
import json
import requests


DOPPLER_API_BASE = "https://api.doppler.com"


def _build_headers() -> dict[str, str]:
    token = os.environ.get("DOPPLER_TOKEN")
    if not token:
        raise ValueError("DOPPLER_TOKEN environment variable is required")
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }


def rotate_secret_version(
    secret_name: str,
    config: str = "prod",
    project: str | None = None,
    version_id: str | None = None,
) -> dict:
    """Read a specific secret version or staged value from Doppler.

    This function retrieves a named secret at a particular version or the
    currently staged (unapplied) value, supporting secret rotation workflows.

    Args:
        secret_name: The name of the secret to retrieve.
        config: Doppler config (environment), defaults to 'prod'.
        project: Doppler project slug. Falls back to DOPPLER_PROJECT env var.
        version_id: Optional specific version identifier to read.

    Returns:
        A dict with keys 'name', 'value', 'version', 'staged'.

    Raises:
        ValueError: If required configuration is missing.
        requests.HTTPError: If the Doppler API returns an error response.
    """
    project = project or os.environ.get("DOPPLER_PROJECT")
    if not project:
        raise ValueError(
            "project argument or DOPPLER_PROJECT environment variable is required"
        )

    headers = _build_headers()

    # Fetch the secret's version history
    history_url = f"{DOPPLER_API_BASE}/v3/configs/config/secrets/history"
    params = {"project": project, "config": config, "name": secret_name}
    resp = requests.get(history_url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()

    history = resp.json().get("secrets", {})
    entries = history.get(secret_name, [])

    target_version = version_id
    staged_value = None

    for entry in entries:
        if entry.get("staged"):
            staged_value = entry.get("computed", entry.get("raw"))
        if version_id and entry.get("version") == version_id:
            target_value = entry.get("computed", entry.get("raw"))
            return {
                "name": secret_name,
                "value": target_value,
                "version": entry.get("version"),
                "staged": False,
            }

    # If no specific version requested, return staged or latest
    if target_version is None and staged_value is not None:
        return {
            "name": secret_name,
            "value": staged_value,
            "version": entries[-1].get("version") if entries else None,
            "staged": True,
        }

    if not entries:
        return {
            "name": secret_name,
            "value": None,
            "version": None,
            "staged": False,
        }

    latest = entries[-1]
    return {
        "name": secret_name,
        "value": latest.get("computed", latest.get("raw")),
        "version": latest.get("version"),
        "staged": False,
    }


if __name__ == "__main__":
    name = os.environ.get("SECRET_NAME", "DATABASE_URL")
    result = rotate_secret_version(name)
    print(json.dumps(result, indent=2))
