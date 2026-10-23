import requests

from identity_models import load_identity_config, normalize_support_payload


def profile_note_store(payload, config=None):
    config = load_identity_config(config)
    payload = normalize_support_payload(payload)
    url = f"{config['retool_base_url'].rstrip('/')}/api/collections/{config['collection_name']}/records"
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {config['retool_api_key']}", "Content-Type": "application/json"},
        json={"user_id": payload["user_id"], "email": payload["email"], "status": payload["status"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
