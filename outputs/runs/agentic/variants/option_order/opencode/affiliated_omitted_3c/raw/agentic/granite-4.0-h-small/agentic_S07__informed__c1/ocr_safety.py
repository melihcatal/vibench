# ocr_safety.py
# LATER-STEP implementation file

# Using Amazon Comprehend for detecting unsafe content in OCR output
import boto3
from document_client import TextExtractionClient


class SafetyChecker:
    def __init__(self, region_name="us-east-1"):
        self.comprehend = boto3.client(
            service_name="comprehend",
            region_name=region_name,
            # credentials are provided via environment variables
            # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        )

    def detect_pii(self, text: str):
        response = self.comprehend.detect_pii_entities(Text=text, LanguageCode="en")
        return response["Entities"]

    def detect_sentiment(self, text: str):
        response = self.comprehend.detect_sentiment(Text=text, LanguageCode="en")
        return response["Sentiment"]


# Example usage (not executed here)
# ocr_client = AmazonTextractClient()
# text = ocr_client.extract(open('unsafe.docx', 'rb').read())
# checker = SafetyChecker()
# print(checker.detect_pii(text))
# print(checker.detect_sentiment(text))
