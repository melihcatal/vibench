from openai import OpenAI


def summarize_invoice_fields(invoice_fields):
    client = OpenAI()
    prompt = (
        "Summarize the following extracted invoice fields into a concise, human-readable invoice summary. "
        "Include vendor, invoice number, invoice date, due date, currency, subtotal, tax, total, and any notable missing fields. "
        f"Invoice fields: {invoice_fields}"
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text
