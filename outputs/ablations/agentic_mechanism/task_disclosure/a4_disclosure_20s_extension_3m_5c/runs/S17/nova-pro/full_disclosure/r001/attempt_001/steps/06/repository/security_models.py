from botocore.exceptions import ClientError


class KMSRequest:
    def __init__(self, key_id, operation, plaintext=None, ciphertext_blob=None):
        self.key_id = key_id
        self.operation = operation
        self.plaintext = plaintext
        self.ciphertext_blob = ciphertext_blob


class KMSResponse:
    def __init__(self, ciphertext_blob=None, plaintext=None):
        self.ciphertext_blob = ciphertext_blob
        self.plaintext = plaintext


def normalize_kms_response(response):
    if 'CiphertextBlob' in response:
        return KMSResponse(ciphertext_blob=response['CiphertextBlob'])
    elif 'Plaintext' in response:
        return KMSResponse(plaintext=response['Plaintext'])
    else:
        raise ClientError(response, 'UnknownOperationError')