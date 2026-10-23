# extract_text.py
# SAME-SCENARIO implementation file

# Using Amazon Textract for OCR
import boto3
from document_client import TextExtractionClient


class AmazonTextractClient(TextExtractionClient):
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client(
            service_name="textract",
            region_name=region_name,
            # credentials are provided via environment variables
            # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        )

    def extract(self, document_bytes):
        # Amazon Textract synchronous API (DetectDocumentText)
        response = self.client.detect_document_text(Document={"Bytes": document_bytes})
        # Extract plain text from blocks
        text = "".join(
            block["Text"]
            for block in response.get("Blocks", [])
            if block["BlockType"] == "LINE"
        )
        return text


# Example usage (not executed here)
# client = AmazonTextractClient()
# result = client.extract(open('sample.png', 'rb').read())
# print(result)
