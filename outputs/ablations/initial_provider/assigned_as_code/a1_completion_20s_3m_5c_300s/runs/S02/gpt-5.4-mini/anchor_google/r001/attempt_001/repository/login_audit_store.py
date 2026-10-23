import requests


def login_audit_store(payload, config=None):
    response = requests.post(
        f"https://{config['project_id']}.firebaseio.com/federated_login_audit.json",
        params={"auth": config["database_secret"]},
        json=payload["record"],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
