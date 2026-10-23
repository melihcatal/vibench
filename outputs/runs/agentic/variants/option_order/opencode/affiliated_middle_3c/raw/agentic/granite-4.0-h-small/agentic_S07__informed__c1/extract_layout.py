import os
import boto3
from document_client import DocumentClient
from document_models import ExtractLayoutRequest, ExtractLayoutResponse


class ExtractLayout:
    def __init__(self):
        # Initialize AWS client using environment variables
        self.client = boto3.client("textract")
        self.document_client = DocumentClient()

    def extract(self, image_path: str) -> ExtractLayoutResponse:
        """Extract layout blocks, lines, and tables from a document using Amazon Textract.

        Args:
            image_path: Path to the scanned image file.

        Returns:
            ExtractLayoutResponse containing the extracted layout elements.
        """
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = self.client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
        )
        # Normalize response using helper
        normalized = self.document_client.normalize_textract_layout(response)
        return ExtractLayoutResponse(layout=normalized)


if __name__ == "__main__":
    extractor = ExtractLayout()
    result = extractor.extract("sample.png")
    print(result.layout)
