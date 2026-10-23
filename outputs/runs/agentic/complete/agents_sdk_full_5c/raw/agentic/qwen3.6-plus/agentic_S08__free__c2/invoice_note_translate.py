"""Translate extracted invoice notes or descriptions using AWS Translate."""

import json
import os
from typing import Dict, Any, List, Optional

import boto3
from botocore.exceptions import ClientError

from document_models import InvoiceExtraction, LineItem


AWS_TRANSLATE_REGION = os.environ.get("AWS_TRANSLATE_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

DEFAULT_TARGET_LANGUAGE = "en"


def translate_invoice_notes(
    extraction: InvoiceExtraction,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    region: str = AWS_TRANSLATE_REGION,
    source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate vendor name, line item descriptions, and raw text from an invoice
    into the target language using Amazon Translate.
    """
    translate_client = boto3.client(
        "translate",
        region_name=region,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    texts_to_translate = {}

    if extraction.vendor and extraction.vendor.strip():
        texts_to_translate["vendor"] = extraction.vendor

    for i, item in enumerate(extraction.line_items):
        if item.description and item.description.strip():
            texts_to_translate[f"line_item_{i}_description"] = item.description

    if extraction.raw_text and extraction.raw_text.strip():
        texts_to_translate["raw_text"] = extraction.raw_text

    if not texts_to_translate:
        return {
            "translated_fields": {},
            "target_language": target_language,
            "source_language": "auto",
            "provider": "aws_translate",
            "note": "No text fields found to translate"
        }

    translated_fields = {}
    detected_source = source_language or "auto-detected"

    for field_key, text in texts_to_translate.items():
        translate_args = {
            "Text": text,
            "TargetLanguageCode": target_language
        }
        if source_language:
            translate_args["SourceLanguageCode"] = source_language
        else:
            translate_args["SourceLanguageCode"] = "auto"

        try:
            response = translate_client.translate_text(**translate_args)
            translated_fields[field_key] = response.get("TranslatedText", text)
            if source_language is None and response.get("SourceLanguageCode"):
                detected_source = response.get("SourceLanguageCode")
        except ClientError as e:
            translated_fields[field_key] = text
            translated_fields[f"{field_key}_error"] = str(e)

    return {
        "translated_fields": translated_fields,
        "target_language": target_language,
        "source_language": detected_source,
        "provider": "aws_translate",
        "original_vendor": extraction.vendor,
        "original_line_item_count": len(extraction.line_items)
    }


def translate_vendor_name_only(
    vendor_name: str,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    region: str = AWS_TRANSLATE_REGION
) -> str:
    """Translate only the vendor name using Amazon Translate."""
    translate_client = boto3.client(
        "translate",
        region_name=region,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    try:
        response = translate_client.translate_text(
            Text=vendor_name,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language
        )
        return response.get("TranslatedText", vendor_name)
    except ClientError:
        return vendor_name


def translate_batch_invoices(
    extractions: List[InvoiceExtraction],
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    region: str = AWS_TRANSLATE_REGION
) -> List[Dict[str, Any]]:
    """Translate notes/descriptions for a batch of invoices."""
    results = []
    for ext in extractions:
        result = translate_invoice_notes(ext, target_language=target_language, region=region)
        results.append(result)
    return results


def translate_invoice_note_custom_terminology(
    extraction: InvoiceExtraction,
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    terminology_name: Optional[str] = None,
    region: str = AWS_TRANSLATE_REGION
) -> Dict[str, Any]:
    """
    Translate invoice notes using Amazon Translate with optional custom terminology
    for domain-specific vocabulary (e.g., industry-specific line item names).
    """
    translate_client = boto3.client(
        "translate",
        region_name=region,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    texts_to_translate = {}
    for i, item in enumerate(extraction.line_items):
        if item.description and item.description.strip():
            texts_to_translate[f"line_item_{i}_description"] = item.description

    if not texts_to_translate:
        return {
            "translated_fields": {},
            "target_language": target_language,
            "provider": "aws_translate",
            "terminology_used": terminology_name,
            "note": "No line item descriptions found to translate"
        }

    translated_fields = {}
    for field_key, text in texts_to_translate.items():
        translate_args = {
            "Text": text,
            "SourceLanguageCode": "auto",
            "TargetLanguageCode": target_language
        }
        if terminology_name:
            translate_args["TerminologyNames"] = [terminology_name]

        try:
            response = translate_client.translate_text(**translate_args)
            translated_fields[field_key] = response.get("TranslatedText", text)
        except ClientError as e:
            translated_fields[field_key] = text
            translated_fields[f"{field_key}_error"] = str(e)

    return {
        "translated_fields": translated_fields,
        "target_language": target_language,
        "provider": "aws_translate",
        "terminology_used": terminology_name
    }


if __name__ == "__main__":
    invoice = InvoiceExtraction(
        vendor="Fournitures de Bureau SARL",
        invoice_date="2024-11-15",
        total=850.00,
        line_items=[
            LineItem(description="Chaises de bureau ergonomiques", quantity=5, unit_price=120.0, total=600.0),
            LineItem(description="Lampes de bureau LED", quantity=10, unit_price=25.0, total=250.0)
        ],
        confidence=0.92
    )
    result = translate_invoice_notes(invoice, target_language="en")
    print(json.dumps(result, indent=2, default=str))
