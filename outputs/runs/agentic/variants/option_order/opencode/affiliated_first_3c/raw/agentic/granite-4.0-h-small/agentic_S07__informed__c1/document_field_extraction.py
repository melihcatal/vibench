import os
import json
from typing import Dict, Any
import boto3
from aws_encryption_sdk import KMSMasterKeyProvider

# LATER-STEP: document_field_extraction.py

# Provider: Amazon Textract AnalyzeExpense (structured invoice/field extraction)
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


def extract_structured_fields(
    ocr_text: str, field_schema: Dict[str, str]
) -> Dict[str, Any]:
    """Extract structured fields from OCR-normalized document text using Textract AnalyzeExpense.

    Args:
        ocr_text (str): Full plain text obtained from OCR.
        field_schema (Dict[str, str]): Mapping of desired field names to simple regex patterns or keywords.

    Returns:
        Dict[str, Any]: Mapped field name to extracted value.
    """
    textract = boto3.client("textract")
    # Textract AnalyzeExpense works best on PDFs; we will simulate by sending the text as a document
    try:
        response = textract.analyze_document(
            Document={
                "Bytes": ocr_text.encode("utf-8")
            },  # placeholder, actual API expects PDF bytes
            FeatureTypes=["FORMS"],
        )
    except Exception as e:
        raise RuntimeError(f"Textract AnalyzeExpense error: {e}")
    # Simplified extraction: search for keywords in the OCR text
    extracted = {}
    for field, pattern in field_schema.items():
        # Very naive pattern match (replace with regex if needed)
        if pattern.lower() in ocr_text.lower():
            # Grab the next word after the keyword as a simple extraction
            parts = ocr_text.lower().split(pattern.lower())
            if len(parts) > 1 and parts[1].strip():
                extracted[field] = parts[1].split()[0]
        else:
            extracted[field] = None
    return extracted


# Example usage (uncomment to test):
# if __name__ == '__main__':
#     schema = {'InvoiceNumber': 'INV-\d+', 'TotalAmount': '\\$\\d+\\.\\d{2}'}
#     with open('sample.txt', 'r') as f:
#         txt = f.read()
#     print(extract_structured_fields(txt, schema))
