import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class DashboardNoteTranslator:
    def __init__(self):
        self.translate = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def translate_text(self, text: str, target_language: str = "es") -> str:
        try:
            response = self.translate.translate_text(
                Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
            )
            return response["TranslatedText"]
        except ClientError as e:
            return f"Translation error: {str(e)}"

    def batch_translate_texts(
        self, texts: List[str], target_language: str = "es"
    ) -> List[str]:
        try:
            results = []
            for text in texts:
                response = self.translate.translate_text(
                    Text=text,
                    SourceLanguageCode="auto",
                    TargetLanguageCode=target_language,
                )
                results.append(response["TranslatedText"])
            return results
        except ClientError as e:
            return [f"Translation error: {str(e)}"] * len(texts)

    def translate_metric_notes(
        self, notes: List[Dict], target_language: str = "es"
    ) -> List[Dict]:
        texts = [note.get("text", "") for note in notes]
        translated_texts = self.batch_translate_texts(texts, target_language)
        return [
            {
                **note,
                "translated_text": translated_text,
                "target_language": target_language,
            }
            for note, translated_text in zip(notes, translated_texts)
        ]
