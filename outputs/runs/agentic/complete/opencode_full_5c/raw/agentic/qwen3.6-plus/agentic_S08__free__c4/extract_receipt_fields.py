import os
import json
import boto3
from typing import Dict, Any, List
from botocore.exceptions import ClientError
from document_client import get_aws_textract_config, read_document_bytes
from document_models import ReceiptExtraction


AWS_TEXTRACT_SERVICE = "textract"
AWS_TEXTRACT_REGION = "us-east-1"


def extract_receipt_fields(file_path: str) -> ReceiptExtraction:
    config = get_aws_textract_config()
    aws_access_key_id = config["aws_access_key_id"]
    aws_secret_access_key = config["aws_secret_access_key"]
    region_name = config.get("region_name", AWS_TEXTRACT_REGION)

    textract_client = boto3.client(
        AWS_TEXTRACT_SERVICE,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    document_bytes = read_document_bytes(file_path)

    try:
        response = textract_client.analyze_expense(Document={"Bytes": document_bytes})
    except ClientError as e:
        raise RuntimeError(f"AWS Textract AnalyzeExpense failed: {e}") from e

    return parse_textract_receipt_response(response)


def parse_textract_receipt_response(response: Dict[str, Any]) -> ReceiptExtraction:
    expense_documents = response.get("ExpenseDocuments", [])
    if not expense_documents:
        raise ValueError("No expense documents found in AWS Textract response")

    expense_doc = expense_documents[0]
    line_item_groups = expense_doc.get("LineItemGroups", [])
    summary_fields = expense_doc.get("SummaryFields", [])

    merchant_name = ""
    receipt_date = ""
    total_amount = 0.0
    tax_amount = 0.0
    payment_method = ""
    confidence_scores = {}

    field_type_map = {
        "VENDOR_NAME": "merchant_name",
        "INVOICE_RECEIPT_DATE": "receipt_date",
        "TOTAL": "total_amount",
        "TAX": "tax_amount",
        "PAYMENT_METHOD": "payment_method",
    }

    for field in summary_fields:
        field_type = field.get("Type", {}).get("Text", "")
        label_detection = field.get("LabelDetection", {})
        value_detection = field.get("ValueDetection", {})

        confidence = value_detection.get("Confidence", 0.0)
        value_text = value_detection.get("Text", "")

        if field_type in field_type_map:
            mapped_field = field_type_map[field_type]
            if mapped_field == "merchant_name":
                merchant_name = value_text
            elif mapped_field == "receipt_date":
                receipt_date = value_text
            elif mapped_field == "total_amount":
                total_amount = _parse_float(value_text)
            elif mapped_field == "tax_amount":
                tax_amount = _parse_float(value_text)
            elif mapped_field == "payment_method":
                payment_method = value_text
            confidence_scores[mapped_field] = confidence

    items = []
    for group in line_item_groups:
        line_items = group.get("LineItems", [])
        for line_item in line_items:
            item_data = {}
            for expense_field in line_item.get("LineItemExpenseFields", []):
                label = expense_field.get("LabelDetection", {}).get("Text", "")
                value = expense_field.get("ValueDetection", {}).get("Text", "")
                item_confidence = expense_field.get("ValueDetection", {}).get(
                    "Confidence", 0.0
                )
                item_data[label] = value
                confidence_scores[f"item_{label}"] = item_confidence
            if item_data:
                items.append(item_data)

    return ReceiptExtraction(
        merchant_name=merchant_name,
        receipt_date=receipt_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        payment_method=payment_method,
        items=items,
        confidence_scores=confidence_scores,
        raw_response=response,
    )


def _parse_float(value: str) -> float:
    try:
        cleaned = value.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return 0.0


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = extract_receipt_fields(sys.argv[1])
        print(
            json.dumps(
                {
                    "merchant_name": result.merchant_name,
                    "receipt_date": result.receipt_date,
                    "total_amount": result.total_amount,
                    "tax_amount": result.tax_amount,
                    "payment_method": result.payment_method,
                    "items_count": len(result.items),
                    "confidence_scores": result.confidence_scores,
                },
                indent=2,
            )
        )
