from mistralai import MistralClient


def summarize_invoice_fields(invoice_fields):
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    result = client.summarize(invoice_fields)
    return result
