import base64
from security_client import SecurityClient

class EnvelopeEncryptionRequest:
    def __init__(self, plaintext: str, key_id: str, encryption_context: dict = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context if encryption_context is not None else {}

class EnvelopeEncryptionResponse:
    def __init__(self, ciphertext_blob: bytes, encrypted_data_key: bytes, key_id: str, arn: str):
        self.ciphertext_blob = base64.b64encode(ciphertext_blob).decode('utf-8')
        self.encrypted_data_key = base64.b64encode(encrypted_data_key).decode('utf-8')
        self.key_id = key_id
        self.arn = arn

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    client = SecurityClient()
    kms_client = client.get_kms_client()

    # Generate a data key
    generate_data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id,
        EncryptionContext=request.encryption_context,
        KeySpec='AES_256'  # Specify the desired data key spec
    )

    data_key_plaintext = generate_data_key_response['Plaintext']
    encrypted_data_key = generate_data_key_response['CiphertextBlob']

    # Encrypt the actual payload with the data key (simulated here)
    # In a real scenario, you would use a cryptographic library like cryptography.io
    # to perform symmetric encryption with the data_key_plaintext.
    # For this example, we'll just base64 encode the plaintext to simulate encryption.
    # This is NOT real encryption with the data key, but a placeholder for demonstration.
    encrypted_payload_with_data_key = base64.b64encode(request.plaintext.encode('utf-8'))

    return EnvelopeEncryptionResponse(
        ciphertext_blob=encrypted_payload_with_data_key,
        encrypted_data_key=encrypted_data_key,
        key_id=generate_data_key_response['KeyId'],
        arn=generate_data_key_response['Arn']
    )