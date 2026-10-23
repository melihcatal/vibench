import boto3
import translate


def translate_text(text):
    translate_client = boto3.client("translate")
    result = translate_client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode="en"
    )
    return result.get("TranslatedText")
