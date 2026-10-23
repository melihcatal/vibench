import os
from security_client import KmsClient

# Use IBM Key Protect as the concrete provider (identifiable by the service name)
client = KmsClient(
    service="IBM Key Protect",
    instance_id=os.getenv("IBM_KP_INSTANCE_ID"),
    apikey=os.getenv("IBM_KP_APIKEY"),
)


def sign_key(key_id: str, data: bytes) -> bytes:
    """Sign data using a key stored in IBM Key Protect.

    Returns the signature bytes.
    """
    response = client.sign(key_id=key_id, data=data)
    return response["Signature"]


def verify_key(key_id: str, signature: bytes, data: bytes) -> bool:
    """Verify a signature against data using IBM Key Protect.

    Returns True if the signature is valid; otherwise False.
    """
    response = client.verify(key_id=key_id, signature=signature, data=data)
    return response.get("Valid", False)
