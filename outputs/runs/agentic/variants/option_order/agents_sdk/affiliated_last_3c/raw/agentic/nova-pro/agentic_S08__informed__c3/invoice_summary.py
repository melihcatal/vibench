import anthropic

ANTHROPIC_API_KEY = 'your_anthropic_api_key'

def summarize_invoice(invoice_fields):
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    response = client.summarize(invoice_fields)
    # Extract summary from response
    return summary