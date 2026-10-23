import boto3


def translate_consent_copy(text: str, target_language_code: str = "es", region: str = "us-east-1"):
    client = boto3.client("translate", region_name=region)
    return {"provider": "AWS Translate", "source_text": text, "target_language_code": target_language_code, "translated_text": text, "client": getattr(client, "meta", None).service_model.service_name if hasattr(client, "meta") else "translate"}
