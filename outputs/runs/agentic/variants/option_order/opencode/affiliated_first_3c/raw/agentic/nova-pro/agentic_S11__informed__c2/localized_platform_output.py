import boto3


def translate_platform_output(output, target_language):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=output, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
