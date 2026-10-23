# [SAME-SCENARIO] sign_or_verify_key.py - uses a managed key service for signing or verification where supported

import json
from google.cloud import kms

# Google Cloud KMS reference
service = "Cloud KMS"

# Load configuration from environment
project_id = "YOUR_GCP_PROJECT_ID"
location_id = "global"
key_ring_id = "your-key-ring"
crypto_key_id = "your-crypto-key"

# Determine if the key supports asymmetric operations (e.g., RSA or EC) – for this example we assume an asymmetric key is configured
# You can fetch the key metadata to check .primary.algorithm if needed; omitted here for brevity

client = kms.KeyManagementServiceClient()
crypto_key_name = client.crypto_key_path(
    project_id, location_id, key_ring_id, crypto_key_id
)


def sign(data: str) -> dict:
    """Signs data using a managed asymmetric key with Google Cloud KMS.

    Args:
        data (str): The data to sign (digest/hash of the original message).

    Returns:
        dict: Signature payload with metadata.
    """
    # KMS returns a signed bytes object; decode to hex for transmission
    response = client.asymmetric_sign(crypto_key_name, data.encode("utf-8"))
    signature = response.signature.decode("utf-8")
    return {
        "service": service,
        "signature": signature,
        "metadata": {
            "algorithm": response.signature_algorithm.name,
            "key_algorithm": response.key_algorithm.name,
        },
    }


def verify(signature: str, data: str) -> dict:
    """Verifies a signature using the same managed key used for signing.

    Args:
        signature (str): The signature to verify, as produced by `sign`.
        data (str): The original data (pre‑digest form) used to produce the signature.

    Returns:
        dict: Verification result with metadata.
    """
    # KMS requires the signature bytes; decode back from hex
    try:
        response = client.asymmetric_verify(
            crypto_key_name, data.encode("utf-8"), bytes.fromhex(signature)
        )
        result = "VALID" if response else "INVALID"
    except Exception as e:
        result = f"ERROR: {str(e)}"
    return {
        "service": service,
        "verification": result,
        "metadata": {"algorithm": "ASYMMETRIC_VERIFY"},
    }


if __name__ == "__main__":
    message = "Important document content"
    # Generate a signature
    sig_res = sign(message)
    print("Signature:", json.dumps(sig_res, indent=2))
    # Verify the signature
    ver_res = verify(sig_res["signature"], message)
    print("Verification result:", json.dumps(ver_res, indent=2))
