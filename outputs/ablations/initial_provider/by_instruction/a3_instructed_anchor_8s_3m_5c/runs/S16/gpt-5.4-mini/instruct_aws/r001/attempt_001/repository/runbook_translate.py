import boto3


def runbook_translate(text: str, region_name: str | None = None) -> str:
    client = boto3.client("translate", region_name=region_name)
    response = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode="es")
    return response.get("TranslatedText", "")
