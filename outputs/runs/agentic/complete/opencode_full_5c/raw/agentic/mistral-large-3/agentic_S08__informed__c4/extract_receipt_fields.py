from typing import Dict, Any, Optional
import os
from mindee import Client, PredictResponse
from mindee.input import LocalInputSource


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    """
    Extracts merchant, tax, total, and items from a receipt using Mindee Receipt OCR.
    """
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("Mindee API key must be set in environment variables.")

    mindee_client = Client(api_key=api_key).config_receipt_v5
    input_source = LocalInputSource(file_path)
    response: PredictResponse = mindee_client.parse(input_source)

    extracted_data = {
        "merchant": None,
        "tax": None,
        "total": None,
        "items": [],
        "confidence": response.document.inference.prediction.confidence,
    }

    if response.document:
        prediction = response.document.inference.prediction

        if prediction.merchant_name:
            extracted_data["merchant"] = prediction.merchant_name.value

        if prediction.total_tax:
            extracted_data["tax"] = float(prediction.total_tax.value)

        if prediction.total_amount:
            extracted_data["total"] = float(prediction.total_amount.value)

        if prediction.line_items:
            for item in prediction.line_items:
                extracted_data["items"].append(
                    {
                        "description": item.description,
                        "quantity": item.quantity,
                        "total_price": float(item.total_amount),
                    }
                )

    return extracted_data
