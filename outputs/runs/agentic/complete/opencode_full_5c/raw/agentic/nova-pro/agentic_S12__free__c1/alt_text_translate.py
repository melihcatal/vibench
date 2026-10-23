import boto3

client = boto3.client("translate")


def alt_text_translate(text, target_language):
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
