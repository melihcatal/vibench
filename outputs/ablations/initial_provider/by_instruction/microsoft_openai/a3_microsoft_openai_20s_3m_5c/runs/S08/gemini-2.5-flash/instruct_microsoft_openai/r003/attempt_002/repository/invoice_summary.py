import os
from document_client import get_openai_client
from document_models import ExtractedInvoiceFields
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

def summarize_invoice(extracted_invoice: ExtractedInvoiceFields) -> str:
    client = get_openai_client()

    invoice_details = f"""
    Vendor: {extracted_invoice.vendor_name}
    Date: {extracted_invoice.invoice_date}
    Total Amount: {extracted_invoice.total_amount}
    Line Items:
    """
    for item in extracted_invoice.line_items:
        invoice_details += f"- {item.description} (Qty: {item.quantity}, Unit Price: {item.unit_price}, Total: {item.total_price})\n"

    system_message = ChatCompletionSystemMessageParam(content="You are an AI assistant that summarizes invoice details concisely.", role="system")
    user_message = ChatCompletionUserMessageParam(content=f"Summarize the following invoice details:\n{invoice_details}", role="user")

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_SUMMARY_MODEL_NAME", "gpt-4"),
        messages=[
            system_message,
            user_message,
        ]
    )
    return response.choices[0].message.content
