import os
import sys
from security_models import DecryptRequest, DecryptResponse, EncryptionAlgorithm
from security_client import execute_decrypt, get_kms_client


def decrypt_payload(
    ciphertext,
    key_id: str = None,
    encryption_context: dict = None,
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
) -> DecryptResponse:
    request = DecryptRequest(
        ciphertext_blob=ciphertext,
        encryption_context=encryption_context,
        encryption_algorithm=algorithm,
    )
    client = get_kms_client()
    response = execute_decrypt(request, client=client)
    return response


def main():
    ciphertext_input = sys.stdin.buffer.read()
    if not ciphertext_input:
        print("Error: No ciphertext provided on stdin", file=sys.stderr)
        sys.exit(1)
    encryption_context = None
    ctx_file = os.environ.get("ENCRYPTION_CONTEXT_FILE")
    if ctx_file and os.path.exists(ctx_file):
        import json

        with open(ctx_file) as f:
            encryption_context = json.load(f)
    response = decrypt_payload(ciphertext_input, encryption_context=encryption_context)
    sys.stdout.buffer.write(response.plaintext)


if __name__ == "__main__":
    main()
