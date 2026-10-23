from security_client import SecurityClient
from security_models import KeyManagementResponse
import base64


def decrypt_payload(payload: dict, config: dict = None) -> KeyManagementResponse:
    config = config or {}
    security_client = SecurityClient(region_name=config.get("region"))
    response = KeyManagementResponse()
    try:
        ciphertext_blob = base64.b64decode(payload["ciphertext"])
        plaintext = security_client.decrypt_data(
            ciphertext_blob=ciphertext_blob,
            key_id=config["key_id"],
            encryption_context=payload.get("encryption_context")
        )
        response.plaintext = plaintext
        response.success = True
    except Exception as e:
        response.error = str(e)
        response.success = False
    return response
