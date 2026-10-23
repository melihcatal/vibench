import re
from google.cloud import secretmanager

_UNSAFE = re.compile(r"(password|passwd|token|apikey|secret|private key)", re.IGNORECASE)


def check_secret_labels_and_notes(secret_name: str, project_id: str) -> dict:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}"
    secret = client.get_secret(request={"name": name})
    labels = dict(secret.labels)
    notes = getattr(secret, "etag", "") or ""
    unsafe = any(_UNSAFE.search(f"{k} {v}") for k, v in labels.items()) or bool(_UNSAFE.search(notes))
    return {"secret": secret_name, "unsafe": unsafe, "labels": labels}
