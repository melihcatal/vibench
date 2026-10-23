"""
Extract vendor, date, total, and line-item fields from an invoice using AWS Textract.
Provider: AWS Textract (AnalyzeExpense API)
"""

import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Optional, Any

from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse, LineItem


def extract_invoice_fields(
    document_path: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    aws_region: Optional[str] = None,
) -> InvoiceExtractionResponse:
    """
    Extract structured invoice fields using AWS Textract AnalyzeExpense API.
    
    Args:
        document_path: Path to invoice PDF/image file
        document_bytes: Raw bytes of invoice document
        aws_region: AWS region for Textract (default: from AWS_DEFAULT_REGION env)
    
    Returns:
        InvoiceExtractionResponse with extracted fields and confidence scores
    """
    region = aws_region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    
    textract_client = boto3.client(
        "textract",
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    if document_bytes:
        document_source = {"Bytes": document_bytes}
    elif document_path:
        with open(document_path, "rb") as f:
            document_source = {"Bytes": f.read()}
    else:
        raise ValueError("Either document_path or document_bytes must be provided")
    
    try:
        response = textract_client.analyze_expense(
            Document=document_source,
        )
    except ClientError as e:
        raise RuntimeError(f"AWS Textract AnalyzeExpense failed: {e}") from e
    
    return _parse_textract_response(response)


def _parse_textract_response(response: Dict[str, Any]) -> InvoiceExtractionResponse:
    """Parse AWS Textract AnalyzeExpense response into structured InvoiceExtractionResponse."""
    vendor = None
    vendor_confidence = 0.0
    invoice_date = None
    date_confidence = 0.0
    total_amount = None
    total_confidence = 0.0
    line_items: List[LineItem] = []
    
    expense_documents = response.get("ExpenseDocuments", [])
    
    if not expense_documents:
        return InvoiceExtractionResponse(
            vendor=None,
            invoice_date=None,
            total_amount=None,
            line_items=[],
            raw_response=response,
        )
    
    summary_fields = expense_documents[0].get("SummaryFields", [])
    
    for field in summary_fields:
        label = field.get("LabelDetection", {}).get("Text", "")
        value_detection = field.get("ValueDetection", {})
        value_text = value_detection.get("Text", "")
        confidence = value_detection.get("Confidence", 0.0)
        
        if label.lower() in ("vendor", "vendor name", "supplier", "company", "bill to"):
            vendor = value_text
            vendor_confidence = confidence
        elif label.lower() in ("invoice date", "date", "doc date"):
            invoice_date = value_text
            date_confidence = confidence
        elif label.lower() in ("total", "total amount", "amount due", "grand total"):
            try:
                total_amount = float(value_text.replace("$", "").replace(",", "").strip())
            except (ValueError, AttributeError):
                total_amount = value_text
            total_confidence = confidence
    
    line_item_groups = expense_documents[0].get("LineItemGroups", [])
    for group in line_item_groups:
        for line in group.get("LineItems", []):
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_total = None
            
            for line_expense in line.get("LineItemExpenseFields", []):
                label = line_expense.get("LabelDetection", {}).get("Text", "").lower()
                value = line_expense.get("ValueDetection", {}).get("Text", "")
                conf = line_expense.get("ValueDetection", {}).get("Confidence", 0.0)
                
                if "description" in label or "item" in label or "name" in label:
                    item_description = value
                elif "qty" in label or "quantity" in label:
                    try:
                        item_quantity = float(value)
                    except (ValueError, TypeError):
                        item_quantity = value
                elif "unit price" in label or "unit cost" in label or "price" in label:
                    try:
                        item_unit_price = float(value.replace("$", "").replace(",", "").strip())
                    except (ValueError, TypeError):
                        item_unit_price = value
                elif "total" in label or "amount" in label or "extended" in label:
                    try:
                        item_total = float(value.replace("$", "").replace(",", "").strip())
                    except (ValueError, TypeError):
                        item_total = value
            
            if item_description is not None:
                line_items.append(
                    LineItem(
                        description=item_description,
                        quantity=item_quantity,
                        unit_price=item_unit_price,
                        line_total=item_total,
                    )
                )
    
    return InvoiceExtractionResponse(
        vendor=vendor,
        invoice_date=invoice_date,
        total_amount=total_amount,
        line_items=line_items,
        vendor_confidence=vendor_confidence,
        date_confidence=date_confidence,
        total_confidence=total_confidence,
        raw_response=response,
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_invoice_fields.py <invoice_file_path>")
        sys.exit(1)
    
    result = extract_invoice_fields(document_path=sys.argv[1])
    print(result.model_dump_json(indent=2))
