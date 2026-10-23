import json

from security_client import from_b64, get_kms_client, normalize_encryption_context
from security_models import OperationResult, normalize_text


def decrypt_payload(ciphertext_b64, encryption_context=None):
    client = get_kms_client()
    response = client.decrypt(
        CiphertextBlob=from_b64(ciphertext_b64),
        EncryptionContext=normalize_encryption_context(encryption_context),
    )
    plaintext = response["Plaintext"].decode("utf-8")
    return OperationResult(ok=True, data={"plaintext": normalize_text(plaintext)})


def main():
    print(json.dumps({"status": "ready"}))


if __name__ == "__main__":
    main()
