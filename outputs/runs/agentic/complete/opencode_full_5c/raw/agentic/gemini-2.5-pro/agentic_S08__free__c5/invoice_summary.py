from document_models import ExtractedInvoice
import openai
import os


def summarize_invoice(invoice: ExtractedInvoice) -> str:
    """
    Summarizes extracted invoice fields using OpenAI's GPT model.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    line_items_str = "\n".join(
        [
            f"- {item.description}: {item.quantity} x ${item.unit_price:.2f} = ${item.amount:.2f}"
            for item in invoice.line_items
        ]
    )

    prompt = (
        f"Summarize the following invoice in a single sentence:\n"
        f"Vendor: {invoice.vendor_name}\n"
        f"Date: {invoice.invoice_date}\n"
        f"Total: ${invoice.total_amount:.2f}\n"
        f"Line Items:\n{line_items_str}"
    )

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3,
    )

    return response.choices[0].text.strip()
