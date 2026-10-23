import os
import boto3
from document_client import DocumentClient
from document_models import FieldExtractionRequest, FieldExtractionResponse


class FieldExtractor:
    def __init__(self):
        # AWS client using environment variables
        self.client = boto3.client("textract")
        self.document_client = DocumentClient()

    def extract(self, image_path: str) -> FieldExtractionResponse:
        """Extract structured fields from OCR-normalized text using Amazon Textract AnalyzeExpense.

        Args:
            image_path: Path to the scanned image file.

        Returns:
            FieldExtractionResponse containing extracted fields as key-value pairs.
        """
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = self.client.analyze_expense(Document={"Bytes": image_bytes})
        # Normalize and extract fields - simplified example
        fields = {}
        for block in response.get("Blocks", []):
            if (
                block["BlockType"] == "KEY_VALUE_SET"
                and block.get("KeyValueOrganization") == "KEY_AFTER_VALUE"
            ):
                key = next(
                    (
                        b["Text"]
                        for b in response["Blocks"]
                        if b["Id"] == block.get("Key", {}).get("Id")
                    ),
                    "",
                )
                value = next(
                    (
                        b["Text"]
                        for b in response["Blocks"]
                        if b["Id"] == block.get("Value", {}).get("Id")
                    ),
                    "",
                )
                fields[key] = value
        return FieldExtractionResponse(fields=fields)


if __name__ == "__main__":
    extractor = FieldExtractor()
    result = extractor.extract("sample_form.png")
    print(result.fields)
