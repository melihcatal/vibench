import boto3

sns_client = boto3.client("sns")


def payload_translate(message, target_language="es"):
    # Placeholder for actual translation logic
    return f"Translated message: {message} to {target_language}"
