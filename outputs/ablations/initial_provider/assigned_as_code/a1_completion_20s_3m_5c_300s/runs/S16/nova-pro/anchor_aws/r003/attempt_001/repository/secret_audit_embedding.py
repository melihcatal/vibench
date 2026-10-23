from security_client import get_secretsmanager_client


def secret_audit_embedding(payload, config=None):
    client = get_secretsmanager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    notes = json.loads(value).get("notes", [])
    embeddings = [embed_note(note) for note in notes]
    return {"embeddings": embeddings}


def embed_note(note):
    # Placeholder for actual embedding logic
    return {"note": note, "embedding": "embedded_value"}