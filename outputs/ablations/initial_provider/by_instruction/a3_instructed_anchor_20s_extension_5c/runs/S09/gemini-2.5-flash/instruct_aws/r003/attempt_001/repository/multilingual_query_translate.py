import boto3
import os
from typing import List

class TranslationClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("translate", region_name=self.region_name)

    def translate_text(self, text: str, source_language_code: str, target_language_code: str) -> str:
        """Translates a single text string using AWS Translate.

        Args:
            text: The text string to translate.
            source_language_code: The language code of the input text (e.g., 'en', 'es').
            target_language_code: The language code to translate the text into (e.g., 'fr', 'de').

        Returns:
            The translated text string.
        """
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return response['TranslatedText']

def multilingual_query_translate(queries: List[str], source_lang: str, target_lang: str) -> List[str]:
    """Translates a list of queries before multilingual embedding search using AWS Translate.

    Args:
        queries: A list of query strings to translate.
        source_lang: The source language code of the queries.
        target_lang: The target language code for translation.

    Returns:
        A list of translated query strings.
    """
    translate_client = TranslationClient()
    translated_queries = []
    for query in queries:
        translated_queries.append(translate_client.translate_text(query, source_lang, target_lang))
    return translated_queries
