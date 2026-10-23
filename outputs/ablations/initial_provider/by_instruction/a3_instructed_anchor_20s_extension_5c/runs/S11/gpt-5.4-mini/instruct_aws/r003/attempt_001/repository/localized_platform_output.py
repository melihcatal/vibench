import boto3


def localized_platform_output(text: str, target_language_code: str = "es"):
    client = boto3.client("translate", region_name=(boto3.session.Session().region_name or "us-east-1"))
    response = client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code)
    return {"text": response.get("TranslatedText", ""), "raw": response}
