from botocore.exceptions import BotoCoreError


def normalize_response(response):
    try:
        return response["Plaintext"].decode("utf-8")
    except BotoCoreError as e:
        raise ValueError("Failed to normalize response") from e
