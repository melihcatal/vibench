from openai import OpenAI
from document_client import get_openai_config
from document_models import InvoiceExtraction
import json

def summarize_invoice(invoice_data: InvoiceExtraction) -> str:
    config = get_openai_config()
    api_key = config.get('api_key')
    if not api_key:
        raise ValueError("OpenAI API key must be configured.")
    
    client = OpenAI(api_key=api_key)

    invoice_dict = invoice_data.__dict__
    # Convert DocumentField objects to their content for better summarization
    if invoice_dict.get('vendor') and hasattr(invoice_dict['vendor'], 'content'):
        invoice_dict['vendor'] = invoice_dict['vendor'].content
    if invoice_dict.get('date') and hasattr(invoice_dict['date'], 'content'):
        invoice_dict['date'] = invoice_dict['date'].content
    if invoice_dict.get('total') and hasattr(invoice_dict['total'], 'content'):
        invoice_dict['total'] = invoice_dict['total'].content
    
    # For line items, extract content for description, quantity, amount
    if 'line_items' in invoice_dict:
        processed_line_items = []
        for item in invoice_dict['line_items']:
            processed_item = {}
            if hasattr(item, 'description') and hasattr(item.description, 'content'):
                processed_item['description'] = item.description.content
            if hasattr(item, 'quantity') and hasattr(item.quantity, 'content'):
                processed_item['quantity'] = item.quantity.content
            if hasattr(item, 'amount') and hasattr(item.amount, 'content'):
                processed_item['amount'] = item.amount.content
            processed_line_items.append(processed_item)
        invoice_dict['line_items'] = processed_line_items

    prompt = f"Summarize the following invoice data in a concise paragraph, highlighting key details like vendor, total amount, date, and a brief overview of line items. Invoice data: {json.dumps(invoice_dict)}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes invoice data."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing invoice with OpenAI: {e}"
