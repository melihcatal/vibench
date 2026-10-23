import os
import base64
from google.cloud import kms_v1
from security_models import KeyManagementRequest, KeyManagementResponse


def encrypt_payload(request: KeyManagementRequest) -> KeyManagementResponse:
    client = kms_v1.KeyManagementServiceClient()
    key_name = request.key_name
    plaintext_bytes = request.plaintext.encode("utf-8")

    try:
        # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; auth=GOOGLE_APPLICATION_CREDENTIALS
        response = client.encrypt(
            request={"name": key_name, "plaintext": plaintext_bytes}
        )
        ciphertext = base64.b64encode(response.ciphertext).decode("utf-8")
        return KeyManagementResponse(ciphertext=ciphertext, success=True)
    except Exception as e:
        return KeyManagementResponse(success=False, message=str(e))
