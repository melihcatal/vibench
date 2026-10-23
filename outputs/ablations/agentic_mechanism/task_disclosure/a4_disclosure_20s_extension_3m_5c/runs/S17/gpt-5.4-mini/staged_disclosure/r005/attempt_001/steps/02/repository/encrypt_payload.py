import base64
import os
from typing import Union

import boto3


def encrypt_payload(plaintext: Union[str, bytes], key_id: str | None = None) -> str:
    kms = boto3.client("kms")
    if isinstance(plaintext, str):
        plaintext_bytes = plaintext.encode("utf-8")
    else:
        plaintext_bytes = plaintext
    if key_id is None:
        key_id = os.environ["AWS_KMS_KEY_ID"]
    response = kms.encrypt(KeyId=key_id, Plaintext=plaintext_bytes)
    return base64.b64encode(response["CiphertextBlob"]).decode("ascii")


def main() -> None:
    plaintext = os.environ["PLAINTEXT_PAYLOAD"]
    print(encrypt_payload(plaintext))


if __name__ == "__main__":
    main()
