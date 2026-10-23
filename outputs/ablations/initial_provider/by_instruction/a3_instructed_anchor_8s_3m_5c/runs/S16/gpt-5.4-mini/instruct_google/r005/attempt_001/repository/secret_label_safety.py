import re

from google.cloud import secretmanager


def secret_label_safety(project_id: str) -> bool:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    unsafe = re.compile(r"(?i)(password|token|secret|private key)")
    for secret in client.list_secrets(request={"parent": parent}):
        for k, v in secret.labels.items():
            if unsafe.search(k) or unsafe.search(v):
                return False
        if getattr(secret, "annotations", None):
            for v in secret.annotations.values():
                if unsafe.search(v):
                    return False
    return True
