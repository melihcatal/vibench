"""Extract vendor, date, total, and line-item fields from an invoice using AWS Textract."""

import os
import boto3
from botocore.exceptions import ClientError
from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse, LineItem


def extract_invoice_fields(request: InvoiceExtractionRequest) -> InvoiceExtractionResponse:
    """Extract structured fields from invoice document using AWS Textract AnalyzeExpense."""
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    textract_client = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    with open(request.document_path, "rb") as document_file:
        document_bytes = document_file.read()

    try:
        response = textract_client.analyze_expense(
            Document={"Bytes": document_bytes}
        )
    except ClientError as exc:
        raise RuntimeError(f"AWS Textract AnalyzeExpense failed: {exc}") from exc

    vendor = _extract_summary_field(response, "VendorName")
    invoice_date = _extract_summary_field(response, "InvoiceDate")
    total_amount = _extract_summary_field(response, "Total")
    invoice_id = _extract_summary_field(response, "InvoiceId")

    line_items = _extract_line_items(response)

    return InvoiceExtractionResponse(
        vendor=vendor,
        invoice_date=invoice_date,
        total_amount=total_amount,
        invoice_id=invoice_id,
        line_items=line_items,
        confidence=response.get("ExpenseDocuments", [{}])[0].get("SummaryFields", [{}])[0].get("ValueDetection", {}).get("Confidence", 0.0) if response.get("ExpenseDocuments") else 0.0,
        provider="aws_textract",
    )


def _extract_summary_field(response: dict, field_name: str) -> str:
    """Extract a specific summary field from AWS Textract AnalyzeExpense response."""
    expense_docs = response.get("ExpenseDocuments", [])
    if not expense_docs:
        return ""

    summary_fields = expense_docs[0].get("SummaryFields", [])
    for field in summary_fields:
        label = field.get("LabelDetection", {}).get("Text", "")
        if label and field_name.lower() in label.lower():
            return field.get("ValueDetection", {}).get("Text", "")
    return ""


def _extract_line_items(response: dict) -> list[LineItem]:
    """Extract line items from AWS Textract AnalyzeExpense response."""
    expense_docs = response.get("ExpenseDocuments", [])
    if not expense_docs:
        return []

    line_item_groups = expense_docs[0].get("LineItemGroups", [])
    items = []
    for group in line_item_groups:
        line_items = group.get("LineItems", [])
        for item in line_items:
            line_item_fields = item.get("LineItemExpenseFields", [])
            description = ""
            quantity = ""
            unit_price = ""
            total_price = ""

            for field in line_item_fields:
                label = field.get("LabelDetection", {}).get("Text", "").lower()
                value = field.get("ValueDetection", {}).get("Text", "")
                if "description" in label or "item" in label:
                    description = value
                elif "quantity" in label or "qty" in label:
                    quantity = value
                elif "price" in label and "unit" in label:
                    unit_price = value
                elif "total" in label or "amount" in label:
                    total_price = value

            items.append(
                LineItem(
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                )
            )

    return items


if __name__ == "__main__":
    req = InvoiceExtractionRequest(document_path="sample_invoice.pdf")
    result = extract_invoice_fields(req)
    print(result)
