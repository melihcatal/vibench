from google.cloud import kms


def get_client():
    return kms.KeyManagementServiceClient()


def normalize_response(response):
    return (
        response.ciphertext if hasattr(response, "ciphertext") else response.plaintext
    )
