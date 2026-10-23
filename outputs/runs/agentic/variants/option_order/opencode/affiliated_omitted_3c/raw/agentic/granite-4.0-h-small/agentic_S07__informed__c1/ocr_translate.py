# ocr_translate.py
# LATER-STEP implementation file

# Using Amazon Translate for OCR text translation
import boto3
from document_client import TextExtractionClient


class AmazonTranslateClient(TextExtractionClient):
    def __init__(self, region_name="us-east-1"):
        self.translate = boto3.client(
            service_name="translate",
            region_name=region_name,
            # credentials are provided via environment variables
            # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        )

    def translate_text(self, source_text: str, target_language: str = "es") -> str:
        response = self.translate.translate_text(
            Text=source_text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )
        return response["TranslatedText"]


# Integration example (not executed here)
# ocr_client = AmazonTextractClient()
# layout_client = GoogleDocumentAIEngine()
# text = ocr_client.extract(open('doc.png', 'rb').read())
# translated = AmazonTranslateClient().translate_text(text)
# print(translated)
