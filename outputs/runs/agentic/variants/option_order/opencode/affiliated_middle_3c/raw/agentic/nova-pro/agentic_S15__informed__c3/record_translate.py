import boto3

TRANSLATE_REGION = os.getenv("AWS_REGION")


def get_translate_client():
    return boto3.client("translate", region_name=TRANSLATE_REGION)


def translate_text(text, source_language_code, target_language_code):
    client = get_translate_client()
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return response["TranslatedText"]
