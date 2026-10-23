import os
import boto3
from botocore.exceptions import NoCredentialsError


def log_message_translate(log_message, target_language):
    client = boto3.client("translate", region_name="us-west-2")
    try:
        response = client.translate_text(
            Text=log_message,
            SourceLanguageCode="en",
            TargetLanguageCode=target_language,
        )
        return response["TranslatedText"]
    except NoCredentialsError:
        return "No AWS credentials found"
