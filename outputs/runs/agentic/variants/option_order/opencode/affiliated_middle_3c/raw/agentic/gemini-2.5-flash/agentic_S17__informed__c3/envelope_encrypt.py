from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> tuple[bytes, bytes]:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )
    # The plaintext bytes to encrypt.
    plaintext = request.plaintext

    # The encrypt method will generate a new data encryption key (DEK)
    # encrypt it with the KMS key, and return both the encrypted DEK and the
    # ciphertext of the original plaintext.
    response = client.encrypt_a_few_words(
        request={"name": key_name, "plaintext": plaintext}
    )

    # Note: For actual envelope encryption, you would typically generate a data key
    # encrypt it with KMS, and then use the data key to encrypt your data locally.
    # The `encrypt_a_few_words` method is a simplified example. For full envelope
    # encryption with a generated data key, you would use `generate_data_encryption_key`
    # and then a local encryption library.

    # For this example, we'll return the ciphertext and the encrypted data encryption key (DEK)
    # as if KMS performed both steps (which `encrypt_a_few_words` essentially simulates for small data).
    return response.ciphertext, response.wrapped_key
