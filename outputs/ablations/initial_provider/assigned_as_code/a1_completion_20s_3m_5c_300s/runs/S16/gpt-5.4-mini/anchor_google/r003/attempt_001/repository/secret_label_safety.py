from google.cloud import secretmanager

from security_client import load_config, secret_name, get_client


def secret_label_safety(payload, config=None):
    config = load_config(config)
    client = get_client()
    name = secret_name(config["project_id"], payload["secret_id"], config["version"])
    response = client.access_secret_version(request={"name": name})
    text = response.payload.data.decode("utf-8")
    unsafe = any(token in text.lower() for token in ["password", "token", "secret", "private key"])
    return {"safe": not unsafe, "note": payload.get("note", ""), "label": payload.get("label", "")}
