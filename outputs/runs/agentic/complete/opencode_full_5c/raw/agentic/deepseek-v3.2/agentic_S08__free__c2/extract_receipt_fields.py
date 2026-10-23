import os
import json
from typing import Dict, Any, List, Optional
import requests
from document_client import get_google_vision_client
from document_models import ReceiptExtractionRequest, ReceiptExtractionResult


def extract_receipt_fields(
    image_path: str, receipt_type: str = "standard"
) -> ReceiptExtractionResult:
    """
    Extract merchant, tax, total, and items from a receipt using Google Cloud Vision.
    """
    try:
        client = get_google_vision_client()

        with open(image_path, "rb") as f:
            content = f.read()

        image = client.image(content=content)

        response = image.document_text_detection()
        document = response.full_text_annotation

        extracted_text = document.text if document else ""

        merchant_name = ""
        tax_amount = None
        total_amount = None
        items = []

        lines = extracted_text.split("\n")

        for i, line in enumerate(lines):
            line_lower = line.lower()

            if not merchant_name and any(
                keyword in line_lower
                for keyword in ["store", "market", "shop", "restaurant", "cafe"]
            ):
                merchant_name = line.strip()

            if "tax" in line_lower or "vat" in line_lower:
                parts = line.split()
                for part in parts:
                    if part.replace(".", "", 1).replace(",", "", 1).isdigit():
                        try:
                            tax_amount = float(part.replace(",", ""))
                            break
                        except:
                            pass

            if (
                "total" in line_lower
                or "amount" in line_lower
                or "balance" in line_lower
            ):
                parts = line.split()
                for part in parts:
                    clean_part = (
                        part.replace("$", "")
                        .replace("€", "")
                        .replace("£", "")
                        .replace(",", "")
                    )
                    if clean_part.replace(".", "", 1).isdigit():
                        try:
                            total_amount = float(clean_part)
                            break
                        except:
                            pass

        for i, line in enumerate(lines):
            line_clean = line.strip()
            if line_clean and len(line_clean) > 3:
                parts = line_clean.split()
                if len(parts) >= 2:
                    last_part = parts[-1]
                    clean_last = (
                        last_part.replace("$", "")
                        .replace("€", "")
                        .replace("£", "")
                        .replace(",", "")
                    )
                    if clean_last.replace(".", "", 1).isdigit():
                        try:
                            price = float(clean_last)
                            item_name = " ".join(parts[:-1])
                            items.append(
                                {"name": item_name, "price": price, "quantity": 1}
                            )
                        except:
                            pass

        return ReceiptExtractionResult(
            merchant=merchant_name,
            tax_amount=tax_amount,
            total_amount=total_amount,
            items=items,
            raw_text=extracted_text,
            confidence_scores={
                "merchant": 0.8 if merchant_name else 0.0,
                "tax": 0.7 if tax_amount is not None else 0.0,
                "total": 0.9 if total_amount is not None else 0.0,
            },
            provider="google_cloud_vision",
            model_used="document_text_detection",
        )

    except Exception as e:
        raise Exception(f"Google Cloud Vision extraction failed: {str(e)}")
