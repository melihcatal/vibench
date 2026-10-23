from openai import OpenAI
from document_client import get_openai_credentials
from typing import Dict, Any

def summarize_invoice_fields(invoice_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using OpenAI GPT.
    """
    creds = get_openai_credentials()
    client = OpenAI(api_key=creds["api_key"])

    prompt = f"Please summarize the following invoice data:
    Vendor: {invoice_data.get('vendor_info', {}).get('name', 'N/A')}
    Date: {invoice_data.get('transaction_date', 'N/A')}
    Total: {invoice_data.get('total_amount', 'N/A')}
    Line Items: "

    for item in invoice_data.get('line_items', []) :
        prompt += f"\n - {item.get('description', 'N/A')}: {item.get('total_price', 'N/A')}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes invoice information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing invoice: {e}"
