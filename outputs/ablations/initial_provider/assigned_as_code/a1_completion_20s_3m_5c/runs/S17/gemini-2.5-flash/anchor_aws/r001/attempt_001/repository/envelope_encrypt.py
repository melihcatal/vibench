import boto3
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    client = boto3.client("kms", region_name=request.region)
    response = client.generate_data_key(
        KeyId=request.key_id,
        EncryptionContext=request.encryption_context or {},
        KeySpec='AES_256'
    )

    data_key_plaintext = response["Plaintext"]
    data_key_ciphertext = response["CiphertextBlob"]

    # In a real scenario, you would use the data_key_plaintext to encrypt your actual data
    # For this example, we'll just return the keys and a dummy ciphertext.
    # For simplicity, we'll use a placeholder for the actual payload encryption
    encrypted_payload_placeholder = b"encrypted_with_data_key:" + request.plaintext

    return EnvelopeEncryptionResponse(
        ciphertext_blob=encrypted_payload_placeholder,
        plaintext_data_key=data_key_plaintext,
        ciphertext_data_key=data_key_ciphertext,
        key_id=request.key_id,
        region=request.region
    )
