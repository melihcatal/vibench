import os
from typing import Dict, List

# Example using AWS Textract for receipt extraction
import boto3


class ReceiptExtractor:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("textract", region_name=region_name)

    def extract(self, receipt_path: str) -> Dict:
        with open(receipt_path, "rb") as f:
            image_bytes = f.read()
        # Call Textract
        response = self.client.detect_document_text(Document={"Bytes": image_bytes})
        # Aggregate fields
        fields = {
            "merchant": "",
            "tax": 0.0,
            "total": 0.0,
            "items": [],
        }
        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                text = block["Text"]
                # Simple heuristics
                if "merchant" in text.lower():
                    fields["merchant"] = text
                elif "tax" in text.lower():
                    try:
                        fields["tax"] = float(text.split(":")[1].strip().replace(",", ""))
                    except Exception:
                        pass
                elif "total" in text.lower():
                    try:
                        fields["total"] = float(text.split(":")[1].strip().replace(",", ""))
                    except Exception:
                        pass
                else:
                    fields["items"].append(text.strip())
        return fields

# Helper function for the scored pipeline
def extract_receipt_fields(receipt_path: str) -> Dict:
    extractor = ReceiptExtractor()
    return extractor.extract(receipt_path)
