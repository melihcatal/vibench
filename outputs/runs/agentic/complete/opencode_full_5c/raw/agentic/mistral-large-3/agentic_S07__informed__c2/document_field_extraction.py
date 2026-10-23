from typing import Dict, List, Optional
import os
import boto3
from botocore.exceptions import ClientError


def document_field_extraction(text: str, document_type: str = "invoice") -> Dict:
    """
    Extracts structured fields from OCR-normalized document text using Amazon Textract AnalyzeExpense.
    """
    if not all([os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY")]):
        raise ValueError("AWS credentials not configured.")

    textract = boto3.client("textract")

    if document_type == "invoice":
        try:
            response = textract.analyze_expense(
                Document={"Bytes": text.encode("utf-8")}
            )

            fields = {}
            for expense_doc in response.get("ExpenseDocuments", []):
                for summary_field in expense_doc.get("SummaryFields", []):
                    field_type = summary_field.get("Type", {}).get("Text", "unknown")
                    field_value = summary_field.get("ValueDetection", {}).get(
                        "Text", ""
                    )
                    fields[field_type] = field_value

            return {"document_type": document_type, "fields": fields}
        except ClientError as e:
            raise ValueError(f"Failed to extract fields: {e}")
    else:
        raise ValueError(f"Unsupported document type: {document_type}")
