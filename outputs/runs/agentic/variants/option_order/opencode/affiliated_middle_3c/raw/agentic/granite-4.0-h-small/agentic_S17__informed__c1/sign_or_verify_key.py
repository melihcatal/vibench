import os
from security_client import KeyManagementClient

# Helper for signing data with a managed key or verifying signatures


def sign_verify_key(data: bytes, key_name: str, mode: str = "sign") -> dict:
    """
    Use Google Cloud KMS to sign data if the key supports signing.
    If mode is "verify", check a signature against the public key.
    Returns provider metadata and result.
    """
    client = KeyManagementClient(service="google-cloud-kms")
    if mode == "sign":
        signature = client.sign(data, key_name)
        result = "signature"
    elif mode == "verify":
        result = client.verify(data, key_name)
    else:
        raise ValueError("mode must be 'sign' or 'verify'")
    return {"result": result, "provider": "Google Cloud KMS", "mode": mode}


if __name__ == "__main__":
    msg = b"message"
    key_id = os.getenv("KMS_SIGNING_KEY_ID")
    # Sign the message
    sig_result = sign_verify_key(msg, key_id, mode="sign")
    print("Signing result:", sig_result)
    # Example verify (requires a signature value)
    # verify_result = sign_verify_key(msg, key_id, mode="verify")
    # print("Verify result:", verify_result)
