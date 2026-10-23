import boto3


def crypto_audit_embedding(ciphertext, audit_note, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    decrypted_text = client.decrypt(CiphertextBlob=ciphertext["ciphertext"])['Plaintext'].decode('utf-8')
    audit_note = f"{audit_note} - Decrypted text: {decrypted_text}"
    return {"audit_note": audit_note}