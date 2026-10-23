import os
from typing import List

import boto3


class QueryTranslator:
    """Translate queries using Amazon Translate."""

    def __init__(self):
        self.client = boto3.client(
            "translate",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source language to target language."""
        response = self.client.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        return response["TranslatedText"]

    def batch_translate(
        self, texts: List[str], source_lang: str, target_lang: str
    ) -> List[str]:
        """Translate a batch of texts."""
        return [self.translate(text, source_lang, target_lang) for text in texts]


def multilingual_query_translate(
    query: str, source_lang: str, target_lang: str = "en"
) -> str:
    """Translate a query for multilingual embedding search."""
    return QueryTranslator().translate(query, source_lang, target_lang)
