import os
import boto3


def invoice_note_translate(note: str, target_lang: str = "en") -> str:
    translate = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )
    result = translate.translate_text(
        Text=note.strip(),
        SourceLanguageCode="auto",
        TargetLanguageCode=target_lang.upper(),
    )
    return result["TranslatedText"]
