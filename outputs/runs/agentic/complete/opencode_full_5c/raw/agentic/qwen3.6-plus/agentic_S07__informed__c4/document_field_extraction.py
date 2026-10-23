import os
from mindee import Client, ProductClient
from mindee.parsing.common import Inference, Prediction
from document_models import OcrResult


MINDEE_API_KEY = os.environ.get("MINDEE_API_KEY", "")


def get_mindee_client():
    return Client(api_key=MINDEE_API_KEY)


def extract_invoice_fields(
    file_bytes: bytes, filename: str = "document.pdf"
) -> Inference:
    client = get_mindee_client()
    product_client = client.product
    with open(filename, "wb") as f:
        f.write(file_bytes)
    input_doc = product_client.source_from_path(filename)
    result = product_client.enqueue_and_parse(input_doc, product="invoice", version="4")
    os.remove(filename)
    return result


def extract_invoice_fields_from_file(file_path: str) -> Inference:
    client = get_mindee_client()
    product_client = client.product
    input_doc = product_client.source_from_path(file_path)
    result = product_client.enqueue_and_parse(input_doc, product="invoice", version="4")
    return result


def extract_fields_from_ocr_text(text: str) -> dict:
    import tempfile

    client = get_mindee_client()
    product_client = client.product
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write(text)
        tmp_path = tmp.name
    input_doc = product_client.source_from_path(tmp_path)
    os.remove(tmp_path)
    return {}


def get_invoice_prediction(inference: Inference) -> Prediction:
    return inference.prediction


def extract_structured_fields(
    file_bytes: bytes, filename: str = "document.pdf"
) -> dict:
    client = get_mindee_client()
    product_client = client.product
    with open(filename, "wb") as f:
        f.write(file_bytes)
    input_doc = product_client.source_from_path(filename)
    result = product_client.enqueue_and_parse(input_doc, product="invoice", version="4")
    os.remove(filename)

    prediction = result.prediction
    fields = {}

    invoice_number = getattr(prediction, "invoice_number", None)
    if invoice_number and getattr(invoice_number, "value", None):
        fields["invoice_number"] = invoice_number.value

    date = getattr(prediction, "date", None)
    if date and getattr(date, "value", None):
        fields["date"] = str(date.value)

    due_date = getattr(prediction, "due_date", None)
    if due_date and getattr(due_date, "value", None):
        fields["due_date"] = str(due_date.value)

    total_amount = getattr(prediction, "total_amount", None)
    if total_amount and getattr(total_amount, "value", None):
        fields["total_amount"] = total_amount.value

    net_amount = getattr(prediction, "net_amount", None)
    if net_amount and getattr(net_amount, "value", None):
        fields["net_amount"] = net_amount.value

    taxes = getattr(prediction, "taxes", None)
    if taxes:
        fields["taxes"] = [
            {"rate": t.rate, "amount": t.amount} for t in taxes if hasattr(t, "rate")
        ]

    supplier = getattr(prediction, "supplier", None)
    if supplier:
        supplier_name = getattr(supplier, "name", None)
        if supplier_name and getattr(supplier_name, "value", None):
            fields["supplier_name"] = supplier_name.value
        supplier_address = getattr(supplier, "address", None)
        if supplier_address and getattr(supplier_address, "value", None):
            fields["supplier_address"] = supplier_address.value

    customer = getattr(prediction, "customer", None)
    if customer:
        customer_name = getattr(customer, "name", None)
        if customer_name and getattr(customer_name, "value", None):
            fields["customer_name"] = customer_name.value

    line_items = getattr(prediction, "line_items", None)
    if line_items:
        fields["line_items"] = []
        for item in line_items:
            item_data = {}
            if hasattr(item, "description") and getattr(
                item.description, "value", None
            ):
                item_data["description"] = item.description.value
            if hasattr(item, "quantity") and getattr(item.quantity, "value", None):
                item_data["quantity"] = item.quantity.value
            if hasattr(item, "unit_price") and getattr(item.unit_price, "value", None):
                item_data["unit_price"] = item.unit_price.value
            if hasattr(item, "total_amount") and getattr(
                item.total_amount, "value", None
            ):
                item_data["total_amount"] = item.total_amount.value
            fields["line_items"].append(item_data)

    return fields
