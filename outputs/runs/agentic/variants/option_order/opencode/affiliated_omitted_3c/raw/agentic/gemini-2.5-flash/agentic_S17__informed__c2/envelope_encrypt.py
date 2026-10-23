from security_client import get_aws_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse
import base64


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms_client = get_aws_kms_client()

    # Generate a data key for envelope encryption
    generate_data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",  # or AES_128
    )
    data_key_plaintext = generate_data_key_response["Plaintext"]
    data_key_ciphertext_blob = generate_data_key_response["CiphertextBlob"]

    # Encrypt the payload with the data key (local encryption)
    # In a real scenario, you would use a symmetric encryption library like cryptography.fernet
    # For this example, we'll simulate with base64 encoding for brevity
    encrypted_payload_bytes = request.plaintext.encode(
        "utf-8"
    )  # Placeholder for actual encryption
    ciphertext_blob = base64.b64encode(encrypted_payload_bytes).decode("utf-8")

    return EnvelopeEncryptResponse(
        ciphertext_blob=ciphertext_blob,
        data_key_ciphertext=base64.b64encode(data_key_ciphertext_blob).decode("utf-8"),
        key_id=request.key_id,
    )
