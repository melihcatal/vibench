import os
import boto3
from document_client import DocumentClient
from document_models import ExtractTablesRequest, ExtractTablesResponse


class ExtractTables:
    def __init__(self):
        # Initialize AWS client using environment variables
        self.client = boto3.client("textract")
        self.document_client = DocumentClient()

    def extract(self, image_path: str) -> ExtractTablesResponse:
        """Extract tables with row and cell structure from a document using Amazon Textract.

        Args:
            image_path: Path to the scanned image file.

        Returns:
            ExtractTablesResponse containing table cells and row information.
        """
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = self.client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
        )
        # Normalize response using helper
        normalized = self.document_client.normalize_textract_tables(response)
        return ExtractTablesResponse(tables=normalized)


if __name__ == "__main__":
    extractor = ExtractTables()
    result = extractor.extract("sample.png")
    print(result.tables)
