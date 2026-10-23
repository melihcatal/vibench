import os
import boto3
from document_client import DocumentClient
from document_models import ExtractKeyValuesRequest, ExtractKeyValuesResponse


class ExtractKeyValues:
    def __init__(self):
        # Initialize AWS client using environment variables
        self.client = boto3.client("textract")
        self.document_client = DocumentClient()

    def extract(self, image_path: str) -> ExtractKeyValuesResponse:
        """Extract key-value pairs from a form-like document using Amazon Textract.

        Args:
            image_path: Path to the scanned image file.

        Returns:
            ExtractKeyValuesResponse containing the extracted key-value pairs.
        """
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = self.client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
        )
        # Normalize response using helper
        normalized = self.document_client.normalize_textract_key_values(response)
        return ExtractKeyValuesResponse(key_values=normalized)


if __name__ == "__main__":
    extractor = ExtractKeyValues()
    result = extractor.extract("sample_form.png")
    print(result.key_values)
