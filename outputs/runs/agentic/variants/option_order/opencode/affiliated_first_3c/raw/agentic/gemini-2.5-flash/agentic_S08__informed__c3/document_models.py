from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

# This file defines local request, response, and normalization helpers for Structured Document Extraction.
# It does not directly integrate with an external provider.


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None


@dataclass
class Amount:
    value: float
    currency: str


@dataclass
class Vendor:
    name: str
    address: Optional[str] = None
    tax_id: Optional[str] = None


@dataclass
class NormalizedExpenseRecord:
    transaction_type: str
    vendor: Vendor
    date: str  # YYYY-MM-DD
    total_amount: Amount
    tax_amount: Optional[Amount] = None
    line_items: List[LineItem] = field(default_factory=list)
    document_type: str  # e.g., "invoice" or "receipt"
    raw_extraction: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentExtractionRequest:
    file_content: bytes
    mime_type: str


@dataclass
class DocumentExtractionResponse:
    extracted_fields: Dict[str, Any]
    document_type: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


# Helper function for converting raw extracted data to a common format (if needed before normalization)
def convert_to_common_format(
    extracted_data: Dict[str, Any], document_type: str
) -> Dict[str, Any]:
    """
    Converts raw extracted data from different providers into a more unified intermediate format
    before full normalization to NormalizedExpenseRecord.
    """
    common_format = {
        "document_type": document_type,
        "vendor": {"name": ""},
        "date": "",
        "total_amount": {"value": 0.0, "currency": ""},
        "tax_amount": {"value": 0.0, "currency": ""},
        "line_items": [],
    }

    if document_type == "invoice":
        common_format["vendor"]["name"] = extracted_data.get("vendor_name", "")
        common_format["date"] = extracted_data.get("invoice_date", "")
        if "total_amount" in extracted_data:
            total_str = extracted_data["total_amount"].replace(" ", "")
            if total_str and len(total_str) > 3:  # Basic check for currency code
                common_format["total_amount"]["value"] = (
                    float(total_str[:-3])
                    if total_str[:-3].replace(".", "", 1).isdigit()
                    else 0.0
                )
                common_format["total_amount"]["currency"] = total_str[-3:]
            else:
                common_format["total_amount"]["value"] = (
                    float(total_str) if total_str.replace(".", "", 1).isdigit() else 0.0
                )
        # More complex line item parsing would go here

    elif document_type == "receipt":
        common_format["vendor"]["name"] = extracted_data.get("merchant_name", "")
        # Receipts often don't have a specific 'invoice_date', using a generic 'date'
        # For simplicity, we are not extracting date from receipt in extract_receipt_fields.py yet.
        common_format["total_amount"]["value"] = (
            float(extracted_data.get("total_amount", 0.0))
            if str(extracted_data.get("total_amount", 0.0))
            .replace(".", "", 1)
            .isdigit()
            else 0.0
        )
        common_format["tax_amount"]["value"] = (
            float(extracted_data.get("tax_amount", 0.0))
            if str(extracted_data.get("tax_amount", 0.0)).replace(".", "", 1).isdigit()
            else 0.0
        )
        # Assume currency is USD for simplicity for receipts if not explicitly extracted
        common_format["total_amount"]["currency"] = "USD"
        common_format["tax_amount"]["currency"] = "USD"
        for item in extracted_data.get("items", []):
            line_item = LineItem(
                description=item.get("description", ""),
                total=float(item.get("price", 0.0))
                if str(item.get("price", 0.0)).replace(".", "", 1).isdigit()
                else 0.0,
            )
            common_format["line_items"].append(line_item)

    return common_format


if __name__ == "__main__":
    # Example usage
    invoice_data = {
        "vendor_name": "Google Cloud",
        "invoice_date": "2023-11-01",
        "total_amount": "500.00 USD",
        "line_items": [],
    }
    receipt_data = {
        "merchant_name": "Starbucks",
        "total_amount": "5.25",
        "tax_amount": "0.50",
        "items": [{"description": "Coffee", "price": "4.75"}],
    }

    common_invoice = convert_to_common_format(invoice_data, "invoice")
    print("Common Invoice Format:", common_invoice)

    common_receipt = convert_to_common_format(receipt_data, "receipt")
    print("Common Receipt Format:", common_receipt)

    # Example of creating a NormalizedExpenseRecord
    vendor_obj = Vendor(name="Example Vendor")
    total_amount_obj = Amount(value=100.00, currency="USD")
    normalized_record = NormalizedExpenseRecord(
        transaction_type="expense",
        vendor=vendor_obj,
        date="2023-11-15",
        total_amount=total_amount_obj,
        document_type="invoice",
    )
    print("Normalized Expense Record:", normalized_record)
