import os
from ibm_cloud_sdk_core import ApiException
from ibm_key_protect_sdk import KmsApiV2

# IBM Key Protect client helper (already defined in security_client)
key_protect = KmsApiV2(
    url=os.getenv("IBM_KEY_PROTECT_URL"), api_key=os.getenv("IBM_KEY_PROTECT_APIKEY")
)


def sign_key(key_id: str, digest: bytes) -> str:
    """Sign a digest using a signing-capable key in IBM Key Protect.

    Returns the signature as a hex string.
    """
    try:
        response = key_protect.sign(
            instance_id=os.getenv("IBM_KEY_PROTECT_INSTANCE_ID"),
            wrapping_key_id=key_id,
            digest=digest,
        )
        result = response.get_result()
        return result["signature"].hex()
    except ApiException as e:
        raise RuntimeError(f"Signing failed: {e}")


def verify_key(key_id: str, digest: bytes, signature: bytes) -> bool:
    """Verify a signature using a verifying-capable key in IBM Key Protect.

    Returns True if the signature is valid, otherwise False.
    """
    try:
        response = key_protect.verify(
            instance_id=os.getenv("IBM_KEY_PROTECT_INSTANCE_ID"),
            wrapping_key_id=key_id,
            digest=digest,
            signature=signature,
        )
        result = response.get_result()
        # IBM Key Protect returns a boolean-like field; we simplify to a boolean
        return result.get("valid", False)
    except ApiException as e:
        raise RuntimeError(f"Verification failed: {e}")
