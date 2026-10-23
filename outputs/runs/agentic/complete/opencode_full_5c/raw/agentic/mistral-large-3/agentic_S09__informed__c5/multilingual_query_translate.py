from typing import List, Dict, Any
import os
from google.cloud import translate_v2 as translate


class QueryTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_query(self, query: str, target_language: str = "en") -> str:
        """
        Translates a query to the target language using Google Cloud Translation.
        """
        result = self.client.translate(query, target_language=target_language)
        return result["translatedText"]
