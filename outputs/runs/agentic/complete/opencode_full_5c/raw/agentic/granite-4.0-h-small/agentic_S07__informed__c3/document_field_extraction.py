import os
import json
from typing import Dict, Any
import boto3
from document_models import DocumentResultModel, normalize_response

# Later-step scored file – structured field extraction from OCR-normalized text
# Uses Amazon Textract AnalyzeExpense (or general AnalyzeDocument) as concrete provider


class DocumentFieldExtraction:
    def __init__(self):
        # Validate AWS credentials environment variables
        for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]:
            if not os.getenv(var):
                raise RuntimeError(f"Missing AWS env var: {var}")
        self.client = boto3.client(
            "textract",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def extract_fields(self, document_result: DocumentResultModel) -> Dict[str, Any]:
        # Textract expects a file bytes or S3 URI; here we mock using bytes (placeholder)
        # In production, replace `self._bytes_from_document` with actual file reading or S3 fetch.
        response = self.client.analyze_document(
            Document={"Bytes": self._bytes_from_document(document_result)},
            FeatureTypes=["FORMS"],
        )
        # Normalize Textract response to our unified model
        return self._normalize_textract(response)

    def _bytes_from_document(self, doc: DocumentResultModel) -> bytes:
        # Placeholder: would normally read the original scanned image bytes
        return b"placeholder image bytes"

    def _normalize_textract(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        # Simple normalization to extract key-value pairs
        fields = {}
        for block in raw.get("Blocks", []):
            if block.get("BlockType") == "KEY_VALUE_SET":
                key_value = next(
                    (
                        item
                        for item in block.get("Relationships", [])
                        if item.get("Type") == "KEY_VALUE"
                    ),
                    None,
                )
                if key_value:
                    kv_type = next(
                        (k for k, v in key_value.items() if v == "KEY"), None
                    )
                    if kv_type:
                        key_text = key_value[kv_type]["Text"]
                        value_text = next(
                            (item["Text"] for item in block.get("Text", []) if item), ""
                        )
                        fields[key_text] = value_text
        return {"extracted_fields": fields, "raw_textract": raw}


if __name__ == "__main__":
    extractor = DocumentFieldExtraction()
    # Use the unified model built from previous steps (here a mock)
    mock_doc = DocumentResultModel(
        text="Sample OCR text with Name: John Doe", layout={}
    )
    fields = extractor.extract_fields(mock_doc)
    print("Extracted fields:", json.dumps(fields, indent=2))
