import boto3


# Translate customer-facing message payload text
def translate_payload(message, target_language):
    translate_client = boto3.client("translate")
    response = translate_client.translate_text(
        Text=message["Message"],
        SourceLanguageCode="en",
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
