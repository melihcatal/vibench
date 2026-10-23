import boto3
import os

client = boto3.client(
    "translate",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def translate_text(text, source_lang, target_lang):
    response = client.translate_text(
        Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]


text = "This is a log message"
translated_text = translate_text(text, "en", "es")
print(translated_text)
