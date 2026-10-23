import os
import openai
from document_models import Invoice


def invoice_summary(invoice: Invoice) -> str:
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"""Summarize the following invoice in a single sentence.
    
    Vendor: {invoice.vendor_name}
    Date: {invoice.invoice_date}
    Total: ${invoice.total_amount:.2f}
    
    Summary:"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes invoices.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=50,
            temperature=0.5,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"
