from document_client import DocumentClients
from document_models import Invoice, Receipt, NormalizedExpense, LineItem
import json

def normalize_expense(extracted_document: (Invoice | Receipt), document_type: str) -> NormalizedExpense:
    clients = DocumentClients()
    if not clients.openai_client:
        raise ValueError("OpenAI client not initialized.")

    if isinstance(extracted_document, Invoice):
        doc_data = {
            "vendor_name": extracted_document.vendor_name,
            "invoice_date": extracted_document.invoice_date,
            "invoice_total": extracted_document.invoice_total,
            "currency": extracted_document.currency,
            "line_items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                }
                for item in extracted_document.line_items
            ]
        }
    elif isinstance(extracted_document, Receipt):
        doc_data = {
            "merchant_name": extracted_document.merchant_name,
            "transaction_date": extracted_document.transaction_date,
            "transaction_time": extracted_document.transaction_time,
            "total_amount": extracted_document.total_amount,
            "tax_amount": extracted_document.tax_amount,
            "currency": extracted_document.currency,
            "line_items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                }
                for item in extracted_document.line_items
            ]
        }
    else:
        raise ValueError("Unsupported document type for normalization.")

    normalized_schema = NormalizedExpense(
        transaction_id="", # This will be generated later or by DB
        document_type=document_type,
        transaction_date="",
        vendor_merchant_name="",
        total_amount=0.0,
        currency="",
        tax_amount=0.0,
        category="",
        description="",
        line_items=[],
        raw_document_data=doc_data,
        validation_status="pending",
        validation_details={},
        notes="",
        memo=""
    )

    prompt = f"""Normalize the following extracted document data into the provided JSON schema. \n\nExtracted Document Data: {json.dumps(doc_data, indent=2)}\n\nTarget Schema for NormalizedExpense (Python dataclass structure provided, convert to JSON):\n{json.dumps({
    "transaction_id": "UUID or identifier",
    "document_type": "invoice" if document_type == "invoice" else "receipt",
    "transaction_date": "YYYY-MM-DD",
    "vendor_merchant_name": "Name of vendor or merchant",
    "total_amount": "Total amount with 2 decimal places",
    "currency": "Currency code (e.g., USD, EUR)",
    "tax_amount": "Tax amount with 2 decimal places",
    "category": "Suggested category (e.g., Travel, Food, Office Supplies)",
    "description": "Brief description of the expense",
    "line_items": [
        {{"description": "Item description", "quantity": 1.0, "unit_price": 10.00, "total_price": 10.00}}
    ],
    "raw_document_data": {{...}}, # The original extracted data
    "validation_status": "pending",
    "validation_details": {{}},
    "notes": "Any relevant notes from the document",
    "memo": "Any memo from the document",
}, indent=2)}\n\nReturn ONLY the JSON object for NormalizedExpense. Do not include any other text or formatting. Fill in all applicable fields from the extracted document data. If a field is not present, use a sensible default or null. For \'description\', provide a concise summary of the transaction. For \'category\', infer a suitable category from the merchant/vendor name or line items. Ensure currency is consistent if multiple currencies appear, prioritize total currency. All monetary values should be floats. Ensure transaction_date is in YYYY-MM-DD format. If line items are missing from source, provide an empty list.  If 'notes' or 'memo' exist in the original document, include them.
"""

    chat_completion = clients.openai_client.chat.completions.create(
        model="gpt-4o-mini", # Using a more capable model for structured output
        messages=[
            {"role": "system", "content": "You are an AI assistant that normalizes extracted document data into a strict JSON schema. You output ONLY the JSON object."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )

    normalized_json = json.loads(chat_completion.choices[0].message.content)

    # Map the JSON back to NormalizedExpense dataclass
    normalized_expense = NormalizedExpense(
        transaction_id=normalized_json.get("transaction_id"),
        document_type=normalized_json.get("document_type"),
        transaction_date=normalized_json.get("transaction_date"),
        vendor_merchant_name=normalized_json.get("vendor_merchant_name"),
        total_amount=normalized_json.get("total_amount"),
        currency=normalized_json.get("currency"),
        tax_amount=normalized_json.get("tax_amount"),
        category=normalized_json.get("category"),
        description=normalized_json.get("description"),
        line_items=[
            LineItem(**item)
            for item in normalized_json.get("line_items", [])
        ] if normalized_json.get("line_items") else [],
        raw_document_data=normalized_json.get("raw_document_data"),
        validation_status=normalized_json.get("validation_status"),
        validation_details=normalized_json.get("validation_details"),
        notes=normalized_json.get("notes"),
        memo=normalized_json.get("memo"),
    )

    return normalized_expense
