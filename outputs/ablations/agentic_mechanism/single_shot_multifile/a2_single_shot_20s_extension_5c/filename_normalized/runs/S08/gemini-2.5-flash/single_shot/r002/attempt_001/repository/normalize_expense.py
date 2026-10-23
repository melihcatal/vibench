import os
from openai import OpenAI
from document_client import get_openai_client
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense

def normalize_expense(extracted_data: InvoiceFields | ReceiptFields) -> NormalizedExpense:
    client = get_openai_client()

    schema = {
        "type": "object",
        "properties": {
            "transaction_type": {"type": "string", "enum": ["invoice", "receipt"]},
            "vendor_name": {"type": "string", "description": "Standardized vendor or merchant name"},
            "transaction_date": {"type": "string", "format": "date", "description": "Transaction date in YYYY-MM-DD format"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string", "description": "Currency code (e.g., USD, EUR)"},
            "tax_amount": {"type": "number", "nullable": True},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "total": {"type": "number"}
                    },
                    "required": ["description", "quantity", "unit_price", "total"]
                }
            },
            "notes": {"type": "string", "nullable": True, "description": "Any additional notes or memos"}
        },
        "required": ["transaction_type", "vendor_name", "transaction_date", "total_amount", "currency", "line_items"]
    }

    if isinstance(extracted_data, InvoiceFields):
        transaction_type = "invoice"
        vendor_name = extracted_data.vendor_name
        transaction_date = extracted_data.invoice_date
        total_amount = extracted_data.total_amount
        currency = extracted_data.currency
        tax_amount = None # Invoices might not always have explicit tax field, can be derived or set to None
        line_items_data = [
            {"description": item.description, "quantity": item.quantity, "unit_price": item.unit_price, "total": item.total}
            for item in extracted_data.line_items
        ]
        notes = None
    elif isinstance(extracted_data, ReceiptFields):
        transaction_type = "receipt"
        vendor_name = extracted_data.merchant_name
        transaction_date = "" # Receipts often lack explicit date field from Textract directly, requires OCR post-processing or LLM
        total_amount = extracted_data.total_amount
        currency = extracted_data.currency
        tax_amount = extracted_data.tax_amount
        line_items_data = [
            {"description": item.description, "quantity": item.quantity, "unit_price": item.price, "total": item.total}
            for item in extracted_data.items
        ]
        notes = None
    else:
        raise ValueError("Unsupported extracted data type")

    # Use LLM to refine and fill in missing/standardize fields if necessary
    # For simplicity, we'll directly map and use LLM for potential date standardization or minor cleanup
    # The main normalization logic is within the function call parameters
    
    prompt_messages = [
        {"role": "system", "content": "You are a helpful assistant that normalizes expense data into a strict JSON schema."},
        {"role": "user", "content": f"Normalize the following expense data:\nType: {transaction_type}\nVendor: {vendor_name}\nDate: {transaction_date}\nTotal: {total_amount} {currency}\nTax: {tax_amount}\nLine Items: {line_items_data}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "normalize_expense_data",
                "description": "Normalize expense data into a standard structured format",
                "parameters": schema
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # Using a capable model for structured output
        messages=prompt_messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "normalize_expense_data"}}
    )

    tool_call = response.choices[0].message.tool_calls[0]
    if tool_call.function.name == "normalize_expense_data":
        normalized_dict = eval(tool_call.function.arguments) # Be careful with eval, ensure input is trustworthy
        return NormalizedExpense(**normalized_dict)
    else:
        raise Exception("OpenAI did not return the expected function call for normalization.")
