from typing import Dict, List, Optional
import os
from google.cloud import translate_v2 as translate


class TranslationClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")
        self.client = translate.Client(project=self.project_id)

    def translate_text(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ) -> str:
        result = self.client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            model="nmt",
        )
        return result["translatedText"]

    def batch_translate_text(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None,
    ) -> List[str]:
        results = self.client.translate(
            texts,
            target_language=target_language,
            source_language=source_language,
            model="nmt",
        )
        return [result["translatedText"] for result in results]
