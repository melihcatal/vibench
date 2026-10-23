import boto3
import os


class ScriptTranslator:
    def __init__(self):
        self.client = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def translate_script(
        self, text: str, source_language: str, target_language: str
    ) -> str:
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        return response["TranslatedText"]
