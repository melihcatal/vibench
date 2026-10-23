"""Extracts vendor, date, total, and line-item fields from an invoice using AWS Textract AnalyzeExpense."""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from document_models import InvoiceExtraction, LineItem, normalize_confidence_score


TEXTRACT_REGION = os.environ.get("AWS_TEXTRACT_REGION", "us-east-1")


def extract_invoice_fields(
    document_bytes: bytes,
    region: str = TEXTRACT_REGION
) -> InvoiceExtraction:
    client = boto3.client(
        "textract",
        region_name=region
    )

    try:
        response = client.analyze_expense(
            Document={"Bytes": document_bytes}
        )
    except ClientError as exc:
        raise RuntimeError(f"AWS Textract AnalyzeExpense failed: {exc}")

    expense_doc = response.get("ExpenseDocuments", [{}])[0]
    line_item_groups = expense_doc.get("LineItemGroups", [])
    summary = expense_doc.get("SummaryFields", [])

    vendor = _extract_field_by_type(summary, "Vendor")
    invoice_date = _extract_field_by_type(summary, "InvoiceDate")
    total = _extract_float_field(summary, "Total")
    tax = _extract_float_field(summary, "Tax")

    line_items: List[LineItem] = []
    for group in line_item_groups:
        items = group.get("LineItems", [])
        for item in items:
            fields = item.get("LineItemExpenseFields", [])
            li = LineItem(
                description=_extract_field_by_type(fields, "Description"),
                quantity=_extract_float_field(fields, "Quantity"),
                unit_price=_extract_float_field(fields, "UnitPrice"),
                total=_extract_float_field(fields, "Total") or 0.0
            )
            line_items.append(li)

    confidence_scores = _collect_confidence_scores(expense_doc)
    overall_confidence = (
        sum(confidence_scores) / len(confidence_scores)
        if confidence_scores else 0.0
    )
    overall_confidence = normalize_confidence_score(
        overall_confidence, provider="aws_textract"
    )

    return InvoiceExtraction(
        vendor=vendor,
        invoice_date=invoice_date,
        total=total or 0.0,
        tax=tax,
        line_items=line_items,
        confidence=overall_confidence,
        raw_text=_build_raw_text(summary)
    )


def _extract_field_by_type(fields: list, target_type: str) -> str:
    for field in fields:
        if field.get("Type", {}).get("Text") == target_type:
            val = field.get("ValueDetection", {})
            return val.get("Text", "")
    return ""


def _extract_float_field(fields: list, target_type: str) -> Optional[float]:
    for field in fields:
        if field.get("Type", {}).get("Text") == target_type:
            val = field.get("ValueDetection", {})
            raw = val.get("Text", "")
            try:
                return float(raw.replace("$", "").replace(",", "").strip())
            except (ValueError, TypeError):
                return None
    return None


def _collect_confidence_scores(expense_doc: Dict[str, Any]) -> List[float]:
    scores = []
    for field in expense_doc.get("SummaryFields", []):
        vd = field.get("ValueDetection", {})
        conf = vd.get("Confidence", 0)
        if conf > 0:
            scores.append(conf / 100.0)
    for group in expense_doc.get("LineItemGroups", []):
        for item in group.get("LineItems", []):
            for lf in item.get("LineItemExpenseFields", []):
                vd = lf.get("ValueDetection", {})
                conf = vd.get("Confidence", 0)
                if conf > 0:
                    scores.append(conf / 100.0)
    return scores


def _build_raw_text(summary_fields: list) -> str:
    parts = []
    for f in summary_fields:
        label = f.get("Type", {}).get("Text", "")
        val = f.get("ValueDetection", {}).get("Text", "")
        if label and val:
            parts.append(f"{label}: {val}")
    return " | ".join(parts)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_invoice_fields.py <pdf_or_image_path>")
        sys.exit(1)
    filepath = sys.argv[1]
    with open(filepath, "rb") as f:
        doc_bytes = f.read()
    result = extract_invoice_fields(doc_bytes)
    print(json.dumps(result.model_dump(), indent=2, default=str))
