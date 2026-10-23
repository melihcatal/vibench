import os
import boto3
from document_client import DocumentClient
from document_models import ExtractTextRequest, ExtractTextResponse


class ExtractText:
    def __init__(self):
        # Initialize AWS client using environment variables
        self.client = boto3.client("textract")
        self.document_client = DocumentClient()

    def extract(self, image_path: str) -> ExtractTextResponse:
        """Extract plain text from a scanned document image using Amazon Textract.

        Args:
            image_path: Path to the scanned image file.

        Returns:
            ExtractTextResponse containing the extracted plain text.
        """
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = self.client.detect_document_text(Document={"Bytes": image_bytes})
        # Normalize response using helper
        normalized = self.document_client.normalize_textract_response(response)
        return ExtractTextResponse(text=normalized["FullText"])


if __name__ == "__main__":
    extractor = ExtractText()
    result = extractor.extract("sample.png")
    print(result.text)
