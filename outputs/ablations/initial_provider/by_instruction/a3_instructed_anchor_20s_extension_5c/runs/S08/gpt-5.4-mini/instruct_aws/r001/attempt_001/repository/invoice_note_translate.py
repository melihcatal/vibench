import boto3


def invoice_note_translate(text: str, target_language: str = "en"):
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language)
    return {"provider": "aws-translate", "translated_text": response.get("TranslatedText"), "target_language": target_language}
