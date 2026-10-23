import base64
import os
from typing import Union

import boto3


def decrypt_payload(ciphertext: Union[str, bytes], key_id: str | None = None) -> str:
    kms = boto3.client("kms")
    if isinstance(ciphertext, str):
        ciphertext_bytes = base64.b64decode(ciphertext)
    else:
        ciphertext_bytes = ciphertext
    kwargs = {"CiphertextBlob": ciphertext_bytes}
    if key_id is not None:
        kwargs["KeyId"] = key_id
    response = kms.decrypt(**kwargs)
    return response["Plaintext"].decode("utf-8")


def main() -> None:
    ciphertext = os.environ["CIPHERTEXT_PAYLOAD"]
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    print(decrypt_payload(ciphertext, key_id))


if __name__ == "__main__":
    main()
