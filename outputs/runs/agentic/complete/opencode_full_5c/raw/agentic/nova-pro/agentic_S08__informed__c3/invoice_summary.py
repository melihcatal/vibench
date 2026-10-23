import mistralai


def summarize_invoice(extracted_data):
    client = mistralai.Client(api_key="your-api-key")
    response = client.create_summary(extracted_data)
    return response
