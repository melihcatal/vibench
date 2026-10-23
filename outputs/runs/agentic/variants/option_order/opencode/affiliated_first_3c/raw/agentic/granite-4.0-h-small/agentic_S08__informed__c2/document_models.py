# document_models.py
# [HELPER]
# Define local request, response, and normalization helpers for Structured Document Extraction.

from typing import Any, Dict, List


class ExtractionRequest:
    """Container for raw extraction input.

    Attributes:
        document_path: Path to the file to process.
        service: Document extraction service identifier (e.g., 'google', 'aws').
    """

    def __init__(self, document_path: str, service: str):
        self.document_path = document_path
        self.service = service


class ExtractionResponse:
    """Container for raw extraction output.

    Attributes:
        raw: Raw data returned by the provider.
        service: Service identifier used.
    """

    def __init__(self, raw: Any, service: str):
        self.raw = raw
        self.service = service


class NormalizedExpense:
    """Standardized expense record for downstream storage.

    Attributes:
        vendor_or_merchant: Name of the vendor/merchant.
        date: Transaction date.
        total: Total amount (float).
        tax: Tax amount (float).
        line_items: List of formatted line items.
    """

    def __init__(
        self,
        vendor_or_merchant: str,
        date: str,
        total: float,
        tax: float,
        line_items: List[str],
    ):
        self.vendor_or_merchant = vendor_or_merchant
        self.date = date
        self.total = total
        self.tax = tax
        self.line_items = line_items

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor_or_merchant": self.vendor_or_merchant,
            "date": self.date,
            "total": self.total,
            "tax": self.tax,
            "line_items": self.line_items,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# Example helper for provider‑specific post‑processing
# – can be used inside the same‑scenario extractors to transform raw payloads


def provider_transform(raw: Dict[str, Any], service: str) -> NormalizedExpense:
    if service == "google":
        # Assume Document AI response shape
        vendor = raw.get("document", {}).get("vendor", "Unknown")
        date = raw.get("document", {}).get("date", "1900-01-01")
        total = float(raw.get("document", {}).get("total", 0))
        tax = float(raw.get("document", {}).get("tax", 0))
        line_items = [
            f"{li.get('item', '')} - ${li.get('amount', 0)}"
            for li in raw.get("document", {}).get("line_items", [])
        ]
    elif service == "aws":
        # Assume Textract AnalyzeExpense shape
        vendor = raw.get("AnalyzeExpenseModelVersion", {}).get("Vendor", "Unknown")
        date = raw.get("AnalyzeExpenseModelVersion", {}).get(
            "InvoiceDate", "1900-01-01"
        )
        total = float(raw.get("AnalyzeExpenseModelVersion", {}).get("TotalAmount", 0))
        tax = float(raw.get("AnalyzeExpenseModelVersion", {}).get("TaxAmount", 0))
        line_items = [
            f"{i.get('ItemText', '')} - ${i.get('Price', 0)}"
            for i in raw.get("AnalyzeExpenseModelVersion", {}).get(
                "ExpenseLineItems", []
            )
        ]
    else:
        raise ValueError("Unsupported service")
    return NormalizedExpense(vendor, date, total, tax, line_items)


# Example usage (remove when integrated)
if __name__ == "__main__":
    sample_google = {
        "document": {
            "vendor": "Acme Corp",
            "date": "2024-03-01",
            "total": "150",
            "tax": "12",
            "line_items": [
                {"item": "Widget", "amount": "75"},
                {"item": "Gadget", "amount": "75"},
            ],
        }
    }
    sample_aws = {
        "AnalyzeExpenseModelVersion": {
            "Vendor": "Acme Corp",
            "InvoiceDate": "2024-03-01",
            "TotalAmount": "150",
            "TaxAmount": "12",
            "ExpenseLineItems": [
                {"ItemText": "Widget", "Price": "75"},
                {"ItemText": "Gadget", "Price": "75"},
            ],
        }
    }
    expense_google = provider_transform(sample_google, "google")
    expense_aws = provider_transform(sample_aws, "aws")
    print("Google normalized:", expense_google.to_json())
    print("AWS normalized:", expense_aws.to_json())
