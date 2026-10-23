import os
from ibm_cloud_sdk_core import ApiException
from ibm_key_protect_sdk import KmsApiV2

# IBM Key Protect client helper (already defined in security_client)
# Assume security_client returns a configured KmsApiV2 instance
key_protect = KmsApiV2(
    url=os.getenv("IBM_KEY_PROTECT_URL"), api_key=os.getenv("IBM_KEY_PROTECT_APIKEY")
)


def decrypt_payload(ciphertext: str, key_id: str) -> str:
    """Decrypt a ciphertext payload using IBM Key Protect.

    Returns the plaintext string.
    """
    try:
        response = key_protect.decrypt(
            instance_id=os.getenv("IBM_KEY_PROTECT_INSTANCE_ID"),
            wrapping_key_id=key_id,
            ciphertext=ciphertext,
        )
        result = response.get_result()
        return result["plaintext"].decode("utf-8")
    except ApiException as e:
        raise RuntimeError(f"Decryption failed: {e}")
