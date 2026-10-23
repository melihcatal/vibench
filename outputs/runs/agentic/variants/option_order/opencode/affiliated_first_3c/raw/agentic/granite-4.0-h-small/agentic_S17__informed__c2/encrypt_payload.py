import os
from ibm_cloud_sdk_core import ApiException
from ibm_key_protect_sdk import KmsApiV2

# IBM Key Protect client helper (already defined in security_client)
# Assume security_client returns a configured KmsApiV2 instance
key_protect = KmsApiV2(
    url=os.getenv("IBM_KEY_PROTECT_URL"), api_key=os.getenv("IBM_KEY_PROTECT_APIKEY")
)


def encrypt_payload(plain_text: str, key_id: str) -> dict:
    """Encrypt a plaintext payload using IBM Key Protect.

    Returns a dictionary with the ciphertext and the key used.
    """
    try:
        response = key_protect.encrypt(
            instance_id=os.getenv("IBM_KEY_PROTECT_INSTANCE_ID"),
            wrapping_key_id=key_id,
            plaintext=plain_text.encode("utf-8"),
        )
        result = response.get_result()
        return {"ciphertext": result["ciphertext"], "key_id": key_id}
    except ApiException as e:
        raise RuntimeError(f"Encryption failed: {e}")
