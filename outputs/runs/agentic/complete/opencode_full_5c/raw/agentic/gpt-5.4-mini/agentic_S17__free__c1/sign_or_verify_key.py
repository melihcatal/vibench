import os

from security_client import SecurityClient


def sign_or_verify_key(
    key_id: str, message: str, signature_b64: str = None, verify: bool = False
):
    client = SecurityClient()
    if verify:
        return client.verify(key_id, message, signature_b64 or "")
    return client.sign(key_id, message)


if __name__ == "__main__":
    key_id = os.environ["AWS_KMS_KEY_ID"]
    print(
        sign_or_verify_key(
            key_id,
            os.environ.get("MESSAGE", ""),
            os.environ.get("SIGNATURE_B64"),
            os.environ.get("VERIFY", "false").lower() == "true",
        )
    )
