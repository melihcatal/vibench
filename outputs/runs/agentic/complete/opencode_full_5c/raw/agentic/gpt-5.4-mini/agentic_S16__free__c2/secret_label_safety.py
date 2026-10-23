from typing import Dict

from security_client import load_security_config, request_json, secret_manager_base_url
from security_models import normalize_secret_name


def secret_label_safety(secret_id: str = "api-key") -> Dict[str, bool]:
    config = load_security_config()
    secret_id = normalize_secret_name(secret_id)
    url = f"{secret_manager_base_url(config)}/{secret_id}"
    response = request_json("GET", url)
    labels = response.get("labels", {})
    notes = response.get("annotations", {})
    unsafe = any(
        "password" in str(v).lower() or "secret" in str(v).lower()
        for v in list(labels.values()) + list(notes.values())
    )
    return {"safe": not unsafe}


if __name__ == "__main__":
    print(secret_label_safety())
