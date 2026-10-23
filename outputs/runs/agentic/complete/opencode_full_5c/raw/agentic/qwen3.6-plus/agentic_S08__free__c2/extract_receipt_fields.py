import boto3
from botocore.exceptions import ClientError
from document_models import ReceiptFields, LineItem
from document_client import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    validate_aws_credentials,
    parse_aws_textract_response,
)


def extract_receipt_fields_from_document(
    document_bytes: bytes,
    mime_type: str = "image/png",
) -> ReceiptFields:
    if not validate_aws_credentials():
        raise ValueError(
            "AWS Textract credentials not configured. "
            "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    textract_client = boto3.client(
        "textract",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    response = textract_client.analyze_expense(Document={"Bytes": document_bytes})

    parsed = parse_aws_textract_response(response)
    raw_text = parsed.get("raw_text", "")

    expense_docs = response.get("ExpenseDocuments", [])
    if not expense_docs:
        return ReceiptFields(
            merchant="Unknown Merchant",
            receipt_date="",
            total_amount=0.0,
            tax_amount=0.0,
            items=[],
            confidence=0.0,
            raw_text=raw_text,
        )

    first_expense = expense_docs[0]
    summary_fields = first_expense.get("SummaryFields", [])
    line_item_groups = first_expense.get("LineItemGroups", [])

    merchant = _find_summary_value(summary_fields, "VENDOR_NAME")
    receipt_date = _find_summary_value(summary_fields, "INVOICE_RECEIPT_DATE")
    total_amount = _find_summary_float(summary_fields, "TOTAL")
    tax_amount = _find_summary_float(summary_fields, "TAX")

    items = _extract_receipt_items(line_item_groups)
    confidence = _calculate_receipt_confidence(first_expense)

    return ReceiptFields(
        merchant=merchant or "Unknown Merchant",
        receipt_date=receipt_date or "",
        total_amount=total_amount or 0.0,
        tax_amount=tax_amount or 0.0,
        items=items,
        confidence=confidence,
        raw_text=raw_text,
    )


def extract_receipt_fields_from_image(
    image_bytes: bytes,
    image_format: str = "png",
) -> ReceiptFields:
    mime_type = f"image/{image_format}"
    return extract_receipt_fields_from_document(image_bytes, mime_type)


def _find_summary_value(summary_fields: list, field_type: str) -> str:
    for field in summary_fields:
        if field.get("Type", {}).get("Text", "").upper() == field_type.upper():
            value_detection = field.get("ValueDetection", {})
            return value_detection.get("Text", "")
    return ""


def _find_summary_float(summary_fields: list, field_type: str) -> float:
    value_str = _find_summary_value(summary_fields, field_type)
    if value_str:
        cleaned = value_str.replace("$", "").replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0


def _extract_receipt_items(line_item_groups: list) -> list[LineItem]:
    items = []
    for group in line_item_groups:
        line_items = group.get("LineItems", [])
        for item in line_items:
            description = ""
            quantity = 1.0
            unit_price = 0.0
            total_price = 0.0
            confidence = 1.0

            for field in item.get("LineItemExpenseFields", []):
                field_type = field.get("Type", {}).get("Text", "").upper()
                value_detection = field.get("ValueDetection", {})
                text_value = value_detection.get("Text", "")
                field_confidence = value_detection.get("Confidence", 100.0) / 100.0

                if field_type == "NAME":
                    description = text_value
                elif field_type == "QUANTITY":
                    try:
                        quantity = float(text_value.replace(",", "").strip())
                    except ValueError:
                        pass
                elif field_type == "UNIT_PRICE":
                    try:
                        unit_price = float(
                            text_value.replace("$", "").replace(",", "").strip()
                        )
                    except ValueError:
                        pass
                elif field_type == "TOTAL":
                    try:
                        total_price = float(
                            text_value.replace("$", "").replace(",", "").strip()
                        )
                    except ValueError:
                        pass

                confidence = min(confidence, field_confidence)

            if description:
                items.append(
                    LineItem(
                        description=description,
                        quantity=quantity,
                        unit_price=unit_price,
                        total=total_price,
                        confidence=confidence,
                    )
                )
    return items


def _calculate_receipt_confidence(expense_doc: dict) -> float:
    summary_fields = expense_doc.get("SummaryFields", [])
    if not summary_fields:
        return 0.0
    confidences = []
    for field in summary_fields:
        value_detection = field.get("ValueDetection", {})
        conf = value_detection.get("Confidence", 0.0) / 100.0
        if conf > 0:
            confidences.append(conf)
    if not confidences:
        return 0.0
    return sum(confidences) / len(confidences)
