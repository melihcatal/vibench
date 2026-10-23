import boto3


def appeal_translate(text, source_language_code="auto", target_language_code="en"):
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language_code if source_language_code != "auto" else "auto", TargetLanguageCode=target_language_code)
    return {"provider": "aws", "translated_text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode", source_language_code), "target_language": target_language_code}
