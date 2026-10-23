import boto3
from typing import Dict, Any


class AWSTranslateClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("translate", region_name=region_name)

    def translate_text(self, text: str, source_language: str, target_language: str) -> Dict[str, Any]:
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        return {"TranslatedText": response["TranslatedText"]}

    def batch_translate_text(self, texts: list[str], source_language: str, target_language: str) -> Dict[str, Any]:
        # AWS Translate doesn't have a direct batch_translate_text API for a list of strings
        # for real-time translation. It has StartTextTranslationJob for asynchronous batch processing.
        # For the purpose of this exercise, we will simulate synchronous batch by iterating.
        # In a real-world scenario, for large batches, StartTextTranslationJob should be used.
        translated_texts = []
        for text in texts:
            response = self.translate_text(text, source_language, target_language)
            translated_texts.append(response["TranslatedText"])
        return {"TranslatedTextList": translated_texts}

    def translate_document(self, content: bytes, source_language: str, target_language: str, file_format: str) -> Dict[str, Any]:
        # AWS Translate supports document translation jobs, but not direct real-time API for markup
        # For this exercise, we'll assume content is text and use translate_text for simplicity
        # In a real scenario, this would involve S3 and StartDocumentTranslationJob
        response = self.translate_text(content.decode('utf-8'), source_language, target_language)
        return {"TranslatedText": response["TranslatedText"]}
