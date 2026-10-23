import boto3
from botocore.exceptions import ClientError


def compliance_note_translate(note, target_language):
    client = boto3.client("translate")
    try:
        response = client.translate_text(
            Text=note, SourceLanguageCode="en", TargetLanguageCode=target_language
        )
        return response["TranslatedText"]
    except ClientError as e:
        print(e)
        return None
