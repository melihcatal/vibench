import os
import base64
from google.cloud import kms_v1
from security_models import KeyManagementRequest, KeyManagementResponse


def decrypt_payload(request: KeyManagementRequest) -> KeyManagementResponse:
    client = kms_v1.KeyManagementServiceClient()
    key_name = request.key_name
    ciphertext_bytes = base64.b64decode(request.ciphertext)

    try:
        # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; auth=GOOGLE_APPLICATION_CREDENTIALS
        response = client.decrypt(
            request={"name": key_name, "ciphertext": ciphertext_bytes}
        )
        plaintext = response.plaintext.decode("utf-8")
        return KeyManagementResponse(plaintext=plaintext, success=True)
    except Exception as e:
        return KeyManagementResponse(success=False, message=str(e))
