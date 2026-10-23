import boto3


def embed_translated_segments(text):
    client = boto3.client("translate")
    result = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode="en"
    )
    return result["TranslatedText"]
