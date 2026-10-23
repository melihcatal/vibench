from document_models import InvoiceExtractionResult
from document_client import get_generative_model_client


def summarize_invoice_fields(
    project_id: str, location: str, invoice_data: InvoiceExtractionResult
) -> str:
    model = get_generative_model_client(
        project_id, location, model_name="gemini-1.5-flash-001"
    )

    # Prepare a concise text input for the LLM based on extracted invoice data
    invoice_details = []
    if invoice_data.vendor_name.value:
        invoice_details.append(f"Vendor: {invoice_data.vendor_name.value}")
    if invoice_data.invoice_date.value:
        invoice_details.append(f"Date: {invoice_data.invoice_date.value}")
    if invoice_data.total_amount.value and invoice_data.currency.value:
        invoice_details.append(
            f"Total: {invoice_data.currency.value} {invoice_data.total_amount.value}"
        )
    if invoice_data.invoice_id.value:
        invoice_details.append(f"Invoice ID: {invoice_data.invoice_id.value}")
    if invoice_data.purchase_order.value:
        invoice_details.append(f"PO: {invoice_data.purchase_order.value}")
    if invoice_data.notes.value:
        invoice_details.append(f"Notes: {invoice_data.notes.value}")

    if invoice_data.line_items:
        line_item_summary = ", ".join(
            [
                f"{item.description} ({item.quantity} x {item.unit_price} = {item.total_price})".strip()
                for item in invoice_data.line_items
                if item.description
            ]
        )
        if line_item_summary:
            invoice_details.append(f"Line Items: {line_item_summary}")

    invoice_text = "; ".join(invoice_details)
    if not invoice_text:
        invoice_text = "No significant invoice details extracted."

    prompt = f"""Summarize the following invoice details concisely, highlighting key information like vendor, total amount, date, and main items. Keep the summary to 2-3 sentences.

Invoice Details: {invoice_text}

Summary:"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
        },
    )

    return response.text
