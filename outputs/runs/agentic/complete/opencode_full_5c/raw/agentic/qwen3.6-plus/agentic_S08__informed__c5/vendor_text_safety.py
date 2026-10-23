import os
import requests
from document_models import InvoiceExtractionResult

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


class TextSafetyResult:
    def __init__(self):
        self.is_safe = True
        self.categories = {}
        self.severity_scores = {}
        self.block_reason = ""
        self.raw_response = None

    def to_dict(self):
        return {
            "is_safe": self.is_safe,
            "categories": self.categories,
            "severity_scores": self.severity_scores,
            "block_reason": self.block_reason,
        }


def moderate_vendor_text(text: str, severity_threshold: int = 4) -> TextSafetyResult:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "must be set for Azure AI Content Safety"
        )

    endpoint_url = (
        f"{AZURE_CONTENT_SAFETY_ENDPOINT.rstrip('/')}"
        f"/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(endpoint_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    result = TextSafetyResult()
    result.raw_response = data

    for category_result in data.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        result.categories[category] = severity
        result.severity_scores[category] = severity

        if severity >= severity_threshold:
            result.is_safe = False
            result.block_reason = f"Category '{category}' exceeded severity threshold ({severity} >= {severity_threshold})"

    return result


def moderate_vendor_notes_from_invoice(
    invoice_result: InvoiceExtractionResult, severity_threshold: int = 4
) -> TextSafetyResult:
    vendor_name = (
        invoice_result.vendor_name.value
        if hasattr(invoice_result.vendor_name, "value")
        else ""
    )
    billing_address = (
        invoice_result.billing_address.value
        if hasattr(invoice_result.billing_address, "value")
        else ""
    )
    invoice_id = (
        invoice_result.invoice_id.value
        if hasattr(invoice_result.invoice_id, "value")
        else ""
    )

    combined_text = f"{vendor_name} {billing_address} {invoice_id}".strip()
    if not combined_text:
        result = TextSafetyResult()
        result.is_safe = True
        return result

    return moderate_vendor_text(combined_text, severity_threshold=severity_threshold)


def moderate_vendor_notes_from_dict(
    invoice_data: dict, severity_threshold: int = 4
) -> TextSafetyResult:
    vendor_name = invoice_data.get("vendor_name", {}).get("value", "")
    billing_address = invoice_data.get("billing_address", {}).get("value", "")
    invoice_id = invoice_data.get("invoice_id", {}).get("value", "")

    combined_text = f"{vendor_name} {billing_address} {invoice_id}".strip()
    if not combined_text:
        result = TextSafetyResult()
        result.is_safe = True
        return result

    return moderate_vendor_text(combined_text, severity_threshold=severity_threshold)
