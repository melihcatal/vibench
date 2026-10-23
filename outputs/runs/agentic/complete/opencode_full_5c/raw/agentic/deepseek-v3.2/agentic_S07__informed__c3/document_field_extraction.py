import os
import boto3
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError


def document_field_extraction(
    image_path: str, region: Optional[str] = None
) -> Dict[str, Any]:
    """Extract structured fields from OCR-normalized document text using Amazon Textract AnalyzeExpense.

    Args:
        image_path: Path to the image file (invoice/receipt)
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        Dictionary with extracted expense fields
    """
    # Read image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Initialize Textract client
    region_name = region or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    client = boto3.client(
        "textract",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        # Call Textract AnalyzeExpense API
        response = client.analyze_expense(Document={"Bytes": image_bytes})

        # Extract expense fields
        expense_documents = response.get("ExpenseDocuments", [])
        if not expense_documents:
            return {}

        # Get first expense document
        expense_doc = expense_documents[0]

        # Extract summary fields
        summary_fields = {}
        for field in expense_doc.get("SummaryFields", []):
            field_type = field.get("Type", {}).get("Text", "").lower()
            field_text = field.get("ValueDetection", {}).get("Text", "")
            confidence = field.get("ValueDetection", {}).get("Confidence", 0.0)

            if field_type and field_text:
                summary_fields[field_type] = {
                    "value": field_text,
                    "confidence": confidence,
                }

        # Extract line item groups
        line_item_groups = []
        for group in expense_doc.get("LineItemGroups", []):
            line_items = []
            for item in group.get("LineItems", []):
                line_item_fields = {}
                for field in item.get("LineItemExpenseFields", []):
                    field_type = field.get("Type", {}).get("Text", "").lower()
                    field_text = field.get("ValueDetection", {}).get("Text", "")
                    confidence = field.get("ValueDetection", {}).get("Confidence", 0.0)

                    if field_type and field_text:
                        line_item_fields[field_type] = {
                            "value": field_text,
                            "confidence": confidence,
                        }
                if line_item_fields:
                    line_items.append(line_item_fields)

            if line_items:
                line_item_groups.append(line_items)

        return {
            "summary_fields": summary_fields,
            "line_item_groups": line_item_groups,
            "vendor": summary_fields.get("vendor", {}).get("value")
            if "vendor" in summary_fields
            else None,
            "total": summary_fields.get("total", {}).get("value")
            if "total" in summary_fields
            else None,
            "invoice_date": summary_fields.get("invoice_date", {}).get("value")
            if "invoice_date" in summary_fields
            else None,
        }

    except ClientError as e:
        raise Exception(f"Textract AnalyzeExpense API error: {e}")
