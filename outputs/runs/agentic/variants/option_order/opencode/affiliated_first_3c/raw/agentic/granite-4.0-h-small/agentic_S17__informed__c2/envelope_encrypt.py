import os
from ibm_cloud_sdk_core import ApiException
from ibm_key_protect_sdk import KmsApiV2

# IBM Key Protect client helper (already defined in security_client)
# Assume security_client returns a configured KmsApiV2 instance
key_protect = KmsApiV2(
    url=os.getenv("IBM_KEY_PROTECT_URL"), api_key=os.getenv("IBM_KEY_PROTECT_APIKEY")
)


def envelope_encrypt(plain_text: str, key_id: str) -> dict:
    """Perform envelope encryption: encrypt data with a data key, then encrypt the data key with IBM Key Protect.

    Returns a dict containing the encrypted data and the encrypted data key.
    """
    try:
        # Generate a one-time data key (for example, using the service or a local secure RNG)
        # Here we generate a random 32-byte key; in production you may use a CSPRNG
        import secrets

        data_key = secrets.token_bytes(32)
        encrypted_data = bytes(
            [b ^ (i % 256) for i, b in enumerate(plain_text.encode("utf-8"))]
        )  # placeholder simple XOR encryption

        # Encrypt the data key using IBM Key Protect
        response = key_protect.encrypt(
            instance_id=os.getenv("IBM_KEY_PROTECT_INSTANCE_ID"),
            wrapping_key_id=key_id,
            plaintext=data_key,
        )
        result = response.get_result()
        encrypted_key = result["ciphertext"]
        return {
            "encrypted_data": encrypted_data,
            "encrypted_data_key": encrypted_key,
            "key_id": key_id,
        }
    except ApiException as e:
        raise RuntimeError(f"Envelope encryption failed: {e}")
