import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def translate_query(query, target_language="es"):
    translate = boto3.client("translate")
    try:
        result = translate.translate_text(
            Text=query, SourceLanguageCode="auto", TargetLanguageCode=target_language
        )
        return result["TranslatedText"]
    except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
        print(f"Error: {e}")
        return None
