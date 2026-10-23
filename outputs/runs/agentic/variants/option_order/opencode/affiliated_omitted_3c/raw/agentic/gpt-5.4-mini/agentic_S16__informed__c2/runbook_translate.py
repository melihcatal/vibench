import boto3
from security_client import resolve_secret_name


def runbook_translate() -> dict:
    client = boto3.client("translate")
    text = resolve_secret_name("RUNBOOK_TEXT", "Rotate the secret carefully.")
    response = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode="es")
    return {"source": text, "translated": response.get("TranslatedText", "")}
