import requests

from identity_models import normalize_profile_claims


def profile_claims(payload, config=None):
    config = config or {}
    access_token = payload["access_token"]
    provider = config.get("provider", "microsoft_graph")
    if provider == "microsoft_graph":
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return normalize_profile_claims(response.json())
    response = requests.get(
        config["userinfo_endpoint"],
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_profile_claims(response.json())
