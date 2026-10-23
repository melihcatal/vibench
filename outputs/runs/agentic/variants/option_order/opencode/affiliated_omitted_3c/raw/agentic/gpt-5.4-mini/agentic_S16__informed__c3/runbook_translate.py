import boto3
from security_models import SecretRequest


def runbook_translate(secret_id: str, text: str, target_language: str) -> str:
    client = boto3.client("translate")
    request = SecretRequest(secret_id=secret_id)
    response = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language)
    return response.get("TranslatedText", "")
