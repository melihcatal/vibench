import os
import google.generativeai as genai


def summarize_invoice_fields(extracted_fields: dict, config=None) -> str:
    config = config or {}
    google_api_key = config.get('GOOGLE_API_KEY', os.environ.get('GOOGLE_API_KEY'))
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY must be provided in config or environment variables.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    vendor_name = extracted_fields.get('vendor', 'N/A')
    invoice_date = extracted_fields.get('date', 'N/A')
    invoice_total = extracted_fields.get('total', 'N/A')
    line_items_summary = []
    for item in extracted_fields.get('line_items', [])[:3]: # Summarize first 3 items
        description = item.get('description', 'N/A')
        quantity = item.get('quantity', 'N/A')
        amount = item.get('amount', 'N/A')
        line_items_summary.append(f"- {description} (Qty: {quantity}, Amt: {amount})")

    prompt = f"""
    Summarize the following invoice details concisely:
    Vendor: {vendor_name}
    Date: {invoice_date}
    Total: {invoice_total}
    Line Items:
    {'; '.join(line_items_summary)}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing invoice: {e}"
