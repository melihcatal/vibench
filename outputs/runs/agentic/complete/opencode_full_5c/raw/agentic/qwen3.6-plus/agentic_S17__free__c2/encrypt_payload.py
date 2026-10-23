import os
import sys
from security_models import EncryptRequest, EncryptResponse, EncryptionAlgorithm
from security_client import execute_encrypt, get_kms_client, serialize_response_for_api


def encrypt_payload(
    plaintext,
    key_id: str,
    encryption_context: dict = None,
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT,
) -> EncryptResponse:
    request = EncryptRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=encryption_context,
        encryption_algorithm=algorithm,
    )
    client = get_kms_client()
    response = execute_encrypt(request, client=client)
    return response


def main():
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        print("Error: AWS_KMS_KEY_ID environment variable is required", file=sys.stderr)
        sys.exit(1)
    plaintext = sys.stdin.buffer.read()
    if not plaintext:
        print("Error: No plaintext provided on stdin", file=sys.stderr)
        sys.exit(1)
    encryption_context = None
    ctx_file = os.environ.get("ENCRYPTION_CONTEXT_FILE")
    if ctx_file and os.path.exists(ctx_file):
        import json

        with open(ctx_file) as f:
            encryption_context = json.load(f)
    response = encrypt_payload(plaintext, key_id, encryption_context)
    output = serialize_response_for_api(response)
    import json

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
