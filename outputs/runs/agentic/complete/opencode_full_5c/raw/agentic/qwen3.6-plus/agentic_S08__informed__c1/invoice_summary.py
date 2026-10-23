import os
import json
from typing import Optional
from document_models import InvoiceFields, expense_record_to_dict

DASHSCOPE_API_KEY_ENV = "DASHSCOPE_API_KEY"
QWEN_MODEL_ID = "qwen-turbo"
QWEN_SUMMARY_MODEL = "qwen-plus"


def summarize_invoice_fields(
    fields: InvoiceFields,
    api_key: Optional[str] = None,
    model: str = QWEN_SUMMARY_MODEL,
) -> dict:
    api_key = api_key or os.environ.get(DASHSCOPE_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(
            f"DashScope API key not found. Set the {DASHSCOPE_API_KEY_ENV} environment variable."
        )

    import dashscope
    from dashscope import Generation

    dashscope.api_key = api_key

    invoice_data = {
        "vendor": fields.vendor_name,
        "invoice_number": fields.invoice_number,
        "invoice_date": fields.invoice_date,
        "due_date": fields.due_date,
        "subtotal": fields.subtotal,
        "tax": fields.tax,
        "total": fields.total,
        "currency": fields.currency,
        "line_items_count": len(fields.line_items),
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "total_price": item.total_price,
            }
            for item in fields.line_items
        ],
    }

    system_prompt = (
        "You are a financial document analyst. Summarize the key details of the provided invoice "
        "in a concise, structured format. Include vendor, date, total, and a brief overview of line items."
    )

    user_prompt = (
        f"Summarize this invoice data:\n{json.dumps(invoice_data, indent=2)}\n\n"
        "Provide a summary with: vendor name, invoice number, date, total amount, "
        "number of line items, and a brief description of what was purchased."
    )

    response = Generation.call(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        result_format="message",
    )

    if response.status_code == 200:
        summary_text = response.output.choices[0].message.content
        return {
            "success": True,
            "summary": summary_text,
            "provider": "dashscope",
            "model": model,
        }
    else:
        return {
            "success": False,
            "error": f"DashScope API error: {response.code} - {response.message}",
            "provider": "dashscope",
            "model": model,
        }


if __name__ == "__main__":
    from document_models import InvoiceFields, LineItem

    sample = InvoiceFields(
        vendor_name="Office Depot",
        invoice_number="INV-2024-5678",
        invoice_date="2024-03-15",
        due_date="2024-04-15",
        subtotal=250.0,
        tax=20.0,
        total=270.0,
        currency="USD",
        line_items=[
            LineItem(
                description="Printer Paper (10 reams)",
                quantity=10,
                unit_price=8.0,
                total_price=80.0,
            ),
            LineItem(
                description="Toner Cartridges",
                quantity=3,
                unit_price=45.0,
                total_price=135.0,
            ),
            LineItem(
                description="Stapler", quantity=1, unit_price=12.0, total_price=12.0
            ),
        ],
    )

    result = summarize_invoice_fields(sample)
    print(json.dumps(result, indent=2))
