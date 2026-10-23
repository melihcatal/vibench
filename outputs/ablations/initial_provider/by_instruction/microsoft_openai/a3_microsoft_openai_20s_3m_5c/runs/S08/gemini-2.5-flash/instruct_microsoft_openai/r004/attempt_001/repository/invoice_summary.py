from document_client import get_openai_client
from document_models import Invoice

def summarize_invoice(invoice: Invoice) -> str:
    client = get_openai_client()

    line_items_summary = "No line items." if not invoice.line_items else \
                         "\n" + "\n".join([f"- {item.description}: {item.total:.2f}" for item in invoice.line_items])

    prompt = f"""Please provide a concise summary of the following invoice:

    Vendor: {invoice.vendor}
    Date: {invoice.date}
    Total Amount: {invoice.total:.2f}
    Line Items: {line_items_summary}

    Focus on the key details: vendor, date, total, and a brief overview of what was purchased.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Using a powerful model for summarization
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes financial documents."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"An error occurred during invoice summarization: {e}")
        raise
