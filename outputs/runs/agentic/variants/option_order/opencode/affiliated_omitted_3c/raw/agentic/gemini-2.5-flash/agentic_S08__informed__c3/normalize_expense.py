import json
from typing import Union, Dict, Any
from document_client import get_openai_client
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense


def normalize_expense(
    extracted_document: Union[ExtractedInvoice, ExtractedReceipt], document_type: str
) -> NormalizedExpense:
    openai_client = get_openai_client()

    # Convert extracted document to a dictionary for LLM input
    extracted_data_dict = {}
    if isinstance(extracted_document, ExtractedInvoice):
        extracted_data_dict["document_type"] = "invoice"
        if extracted_document.vendor_name:
            extracted_data_dict["vendor_name"] = extracted_document.vendor_name.value
        if extracted_document.invoice_date:
            extracted_data_dict["transaction_date"] = (
                extracted_document.invoice_date.value
            )
        if extracted_document.total_amount:
            extracted_data_dict["total_amount"] = extracted_document.total_amount.value
        if extracted_document.currency:
            extracted_data_dict["currency"] = extracted_document.currency.value
        if extracted_document.total_tax:
            extracted_data_dict["tax_amount"] = extracted_document.total_tax.value
        extracted_data_dict["line_items"] = []
        for item in extracted_document.line_items:
            item_dict = {}
            if item.description:
                item_dict["description"] = item.description
            if item.quantity:
                item_dict["quantity"] = item.quantity
            if item.unit_price:
                item_dict["unit_price"] = item.unit_price
            if item.amount:
                item_dict["amount"] = item.amount
            extracted_data_dict["line_items"].append(item_dict)
        # For invoices, we can use vendor_name as a simple memo if no other note field is available for this example.
        extracted_data_dict["memo_field"] = (
            extracted_document.vendor_name.value
            if extracted_document.vendor_name
            else None
        )

    elif isinstance(extracted_document, ExtractedReceipt):
        extracted_data_dict["document_type"] = "receipt"
        if extracted_document.merchant_name:
            extracted_data_dict["vendor_name"] = extracted_document.merchant_name.value
        if extracted_document.transaction_date:
            extracted_data_dict["transaction_date"] = (
                extracted_document.transaction_date.value
            )
        if extracted_document.total_amount:
            extracted_data_dict["total_amount"] = extracted_document.total_amount.value
        if extracted_document.currency:
            extracted_data_dict["currency"] = extracted_document.currency.value
        if extracted_document.total_tax:
            extracted_data_dict["tax_amount"] = extracted_document.total_tax.value
        extracted_data_dict["line_items"] = []
        for item in extracted_document.items:
            item_dict = {}
            if item.description:
                item_dict["description"] = item.description
            if item.quantity:
                item_dict["quantity"] = item.quantity
            if item.price:
                item_dict["unit_price"] = item.price
            if item.total_price:
                item_dict["amount"] = item.total_price
            extracted_data_dict["line_items"].append(item_dict)
        extracted_data_dict["memo_field"] = (
            extracted_document.merchant_name.value
            if extracted_document.merchant_name
            else None
        )

    # Define the target schema for NormalizedExpense
    target_schema = {
        "document_type": "string",
        "vendor_name": "string, optional",
        "transaction_date": "string (YYYY-MM-DD), optional",
        "total_amount": "float, optional",
        "currency": "string, optional",
        "line_items": "list of objects (description: string, quantity: float, unit_price: float, amount: float), optional",
        "tax_amount": "float, optional",
        "memo_field": "string, optional",
        "raw_extraction": "object, optional",  # To store the original extraction for debugging/auditing
    }

    # Craft the prompt for the LLM
    prompt = f"""Normalize the following extracted document data into a JSON object adhering to this schema:\n\n{json.dumps(target_schema, indent=2)}\n\nExtracted Data:\n{json.dumps(extracted_data_dict, indent=2)}\n\nEnsure the output is a valid JSON object. For 'raw_extraction', provide the original Extracted Data as a dictionary."""

    chat_completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",  # Using a powerful model for structured output
        messages=[
            {
                "role": "system",
                "content": "You are an expert at normalizing document extraction data into a specified JSON schema.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    normalized_json_str = chat_completion.choices[0].message.content
    normalized_data = json.loads(normalized_json_str)

    # Add the raw extraction to the normalized data
    normalized_data["raw_extraction"] = extracted_data_dict

    return NormalizedExpense(
        document_type=normalized_data.get("document_type"),
        vendor_name=normalized_data.get("vendor_name"),
        transaction_date=normalized_data.get("transaction_date"),
        total_amount=normalized_data.get("total_amount"),
        currency=normalized_data.get("currency"),
        line_items=normalized_data.get("line_items"),
        tax_amount=normalized_data.get("tax_amount"),
        memo_field=normalized_data.get("memo_field"),
        raw_extraction=normalized_data.get("raw_extraction"),
    )
