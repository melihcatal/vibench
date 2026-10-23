import os
from document_client import get_vertexai_model
from document_models import InvoiceFields

def summarize_invoice(invoice_data: InvoiceFields) -> str:
    model = get_vertexai_model(model_name="text-bison@001")

    # Construct a detailed prompt for summarization
    prompt_parts = [
        "Summarize the following invoice details:",
        f"Vendor: {invoice_data.vendor_name}",
        f"Date: {invoice_data.invoice_date}",
        f"Total Amount: {invoice_data.total_amount} {invoice_data.currency}"
    ]

    if invoice_data.line_items:
        prompt_parts.append("Line Items:")
        for item in invoice_data.line_items:
            prompt_parts.append(f"- {item.description} (Qty: {item.quantity}, Unit Price: {item.unit_price}, Total: {item.total})")

    prompt_parts.append("\nProvide a concise summary highlighting the key information.")

    prompt = "\n".join(prompt_parts)

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
        top_k=40,
        top_p=0.8
    )

    return response.text
