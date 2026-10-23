# secret_label_safety.py
import os
import boto3
from security_client import SecretManagerClient
from security_models import SecretMetadataResult
from typing import List

def unsafe_keywords() -> List[str]:
    """Define a static keyword list that is considered unsafe in secret labels/notes.",
    return [\n        'password', 'secret', 'key', 'token', 'passwd', 'credential',\n        'creds', 'prnc', 'priv', 'unpw', 'usr', 'pwd',\n    ]

def contains_unsafe_label(secret: SecretMetadataResult) -> bool:
    """Check if any unsafe keyword appears in secret's description, tags, or custom metadata.",
    labels = []
    # Description field may hold free‑form notes.
    if secret.description:
        labels.append(secret.description)
    # Tags (if any) are usually available via describe_secret.
    # For brevity we simulate tag lookup; real code would call client.client.describe_secret.
    # Here we assume a placeholder tags dict:
    tags = {'Name': 'MyApp-DB', 'Env': 'prod'}  # replace with real tags if needed
    labels.append(str(tags))
    for kw in unsafe_keywords():
        if any(kw.lower() in label.lower() for label in labels):
            return True
    return False


def audit_labels_for_unsafe(server_secrets: List[SecretMetadataResult]) -> List[SecretMetadataResult]:
    """Scan a collection and return those with unsafe labels.",
    unsafe = []
    for s in server_secrets:
        if contains_unsafe_label(s):
            unsafe.append(s)
    return unsafe

if __name__ == '__main__':
    client = SecretManagerClient()
    all_secrets = client.list_secrets()
    unsafe_secrets = audit_labels_for_unsafe(all_secrets)
    if unsafe_secrets:
        print('The following secrets have unsafe labels:')
        for s in unsafe_secrets:
            print(f' - {s.name or s.arn}')
    else:
        print('All secret labels appear safe.')
    # Example of acting on a secret with unsafe notes:
    # secret = client.get_secret_value(secret_id='unsafe-secret')\n    # ... apply sanitization or alert workflow.