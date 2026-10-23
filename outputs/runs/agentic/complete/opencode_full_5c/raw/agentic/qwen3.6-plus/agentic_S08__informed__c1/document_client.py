import os
from typing import Optional, BinaryIO


MINDEE_API_KEY_ENV = "MINDEE_API_KEY"
MINDEE_INVOICE_PRODUCT = "mindee/invoice"
MINDEE_RECEIPT_PRODUCT = "mindee/expense_receipt"
MINDEE_API_VERSION = "v1"


class MindeeConfig:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get(MINDEE_API_KEY_ENV, "")
        if not self.api_key:
            raise ValueError(
                f"Mindee API key not found. Set the {MINDEE_API_KEY_ENV} environment variable."
            )

    def get_client(self):
        from mindee import Client

        return Client(api_key=self.api_key)


def load_mindee_config(api_key: Optional[str] = None) -> MindeeConfig:
    return MindeeConfig(api_key=api_key)


def parse_invoice_response(mindee_response) -> dict:
    invoice_prediction = mindee_response.document.inference.prediction
    result = {
        "vendor_name": getattr(invoice_prediction, "supplier_name", {}).value or "",
        "vendor_address": getattr(invoice_prediction, "supplier_address", {}).value
        or "",
        "invoice_number": getattr(invoice_prediction, "invoice_number", {}).value or "",
        "invoice_date": getattr(invoice_prediction, "date", {}).value or "",
        "due_date": getattr(invoice_prediction, "due_date", {}).value or "",
        "subtotal": float(getattr(invoice_prediction, "total_net", {}).value or 0.0),
        "tax": float(getattr(invoice_prediction, "total_tax", {}).value or 0.0),
        "total": float(getattr(invoice_prediction, "total_amount", {}).value or 0.0),
        "currency": getattr(invoice_prediction, "locale", {}).currency or "USD",
        "notes": "",
    }

    line_items = []
    for line_item in getattr(invoice_prediction, "line_items", []):
        line_items.append(
            {
                "description": getattr(line_item, "description", {}).value or "",
                "quantity": float(getattr(line_item, "quantity", {}).value or 0.0),
                "unit_price": float(getattr(line_item, "unit_price", {}).value or 0.0),
                "total_price": float(
                    getattr(line_item, "total_amount", {}).value or 0.0
                ),
            }
        )
    result["line_items"] = line_items

    field_confidences = {}
    for field_name in [
        "supplier_name",
        "invoice_number",
        "date",
        "total_amount",
        "total_tax",
    ]:
        field_obj = getattr(invoice_prediction, field_name, None)
        if field_obj and hasattr(field_obj, "confidence"):
            field_confidences[field_name] = float(field_obj.confidence)
    result["field_confidences"] = field_confidences
    result["raw_confidence"] = float(
        mindee_response.document.inference.prediction.confidence or 0.0
    )

    return result


def parse_receipt_response(mindee_response) -> dict:
    receipt_prediction = mindee_response.document.inference.prediction
    result = {
        "merchant_name": getattr(receipt_prediction, "supplier_name", {}).value or "",
        "merchant_address": getattr(receipt_prediction, "supplier_address", {}).value
        or "",
        "receipt_date": getattr(receipt_prediction, "date", {}).value or "",
        "receipt_time": getattr(receipt_prediction, "time", {}).value or "",
        "subtotal": float(getattr(receipt_prediction, "total_net", {}).value or 0.0),
        "tax": float(getattr(receipt_prediction, "total_tax", {}).value or 0.0),
        "tip": float(getattr(receipt_prediction, "tip", {}).value or 0.0),
        "total": float(getattr(receipt_prediction, "total_amount", {}).value or 0.0),
        "currency": getattr(receipt_prediction, "locale", {}).currency or "USD",
        "payment_method": "",
    }

    items = []
    for line_item in getattr(receipt_prediction, "line_items", []):
        items.append(
            {
                "description": getattr(line_item, "description", {}).value or "",
                "quantity": float(getattr(line_item, "quantity", {}).value or 0.0),
                "unit_price": float(getattr(line_item, "unit_price", {}).value or 0.0),
                "total_price": float(
                    getattr(line_item, "total_amount", {}).value or 0.0
                ),
            }
        )
    result["items"] = items

    field_confidences = {}
    for field_name in ["supplier_name", "date", "total_amount", "total_tax"]:
        field_obj = getattr(receipt_prediction, field_name, None)
        if field_obj and hasattr(field_obj, "confidence"):
            field_confidences[field_name] = float(field_obj.confidence)
    result["field_confidences"] = field_confidences
    result["raw_confidence"] = float(
        mindee_response.document.inference.prediction.confidence or 0.0
    )

    return result


def extract_from_file_path(
    client, product: str, file_path: str, version: str = MINDEE_API_VERSION
):
    with open(file_path, "rb") as f:
        doc_source = client.source_from_path(file_path)
        if product == MINDEE_INVOICE_PRODUCT:
            return client.parse(doc_source, product_class="invoice", include_words=True)
        elif product == MINDEE_RECEIPT_PRODUCT:
            return client.parse(
                doc_source, product_class="expense_receipt", include_words=True
            )
        else:
            return client.parse_new(
                doc_source, endpoint_name=product, endpoint_version=version
            )


def extract_from_bytes(
    client,
    product: str,
    file_bytes: bytes,
    filename: str = "document.pdf",
    version: str = MINDEE_API_VERSION,
):
    import io

    doc_source = client.source_from_bytes(file_bytes, filename)
    if product == MINDEE_INVOICE_PRODUCT:
        return client.parse(doc_source, product_class="invoice", include_words=True)
    elif product == MINDEE_RECEIPT_PRODUCT:
        return client.parse(
            doc_source, product_class="expense_receipt", include_words=True
        )
    else:
        return client.parse_new(
            doc_source, endpoint_name=product, endpoint_version=version
        )
