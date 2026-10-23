import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def translate_text(text, source_language, target_language):
    try:
        translate_client = boto3.client("translate")
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        return response.get("TranslatedText", "")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return ""
