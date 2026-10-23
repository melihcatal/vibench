import os
from document_models import Invoice, Receipt, NormalizedExpense, LineItem, ReceiptItem
from document_client import get_vertex_ai_model
from vertexai.generative_models import Part, GenerationConfig
import json

def normalize_expense(extracted_data: dict, config: dict = None) -> NormalizedExpense:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    model = get_vertex_ai_model(project_id, location, "gemini-1.5-flash-001")

    document_type = None
    if "invoices" in extracted_data and extracted_data["invoices"]:
        document_type = "invoice"
        raw_data = extracted_data["invoices"][0]
        invoice = Invoice(**raw_data)
        normalized_line_items = [
            LineItem(description=item.description, quantity=item.quantity, amount=item.amount)
            for item in invoice.line_items
        ]
        prompt_text = f"Normalize the following invoice data into a JSON object adhering to the NormalizedExpense schema. Ensure currency is inferred or defaulted to USD if not present. Invoice data: {json.dumps(invoice.dict(by_alias=True, exclude_none=True))}"
    elif "receipts" in extracted_data and extracted_data["receipts"]:
        document_type = "receipt"
        raw_data = extracted_data["receipts"][0]
        receipt = Receipt(**raw_data)
        normalized_line_items = [
            LineItem(description=item.description, quantity=item.quantity, amount=item.amount if item.amount else (item.quantity * item.price if item.quantity and item.price else None))
            for item in receipt.items
        ]
        prompt_text = f"Normalize the following receipt data into a JSON object adhering to the NormalizedExpense schema. Ensure currency is inferred or defaulted to USD if not present. Receipt data: {json.dumps(receipt.dict(by_alias=True, exclude_none=True))}"
    else:
        raise ValueError("No recognized document type (invoice or receipt) found in extracted data.")

    response = model.generate_content(
        [prompt_text, Part.from_text(NormalizedExpense.schema_json())],
        generation_config=GenerationConfig(response_mime_type="application/json")
    )
    
    normalized_data_json = json.loads(response.text)
    normalized_data = NormalizedExpense(
        document_type=document_type,
        vendor_name=normalized_data_json.get("vendor_name"),
        transaction_date=normalized_data_json.get("transaction_date"),
        total_amount=normalized_data_json.get("total_amount"),
        currency=normalized_data_json.get("currency", "USD"),
        description=normalized_data_json.get("description"),
        line_items=normalized_line_items,
        original_data=raw_data
    )

    return normalized_data
