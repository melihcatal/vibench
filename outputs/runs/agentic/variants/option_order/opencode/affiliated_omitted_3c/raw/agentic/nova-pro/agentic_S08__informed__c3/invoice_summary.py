import mistralai


def summarize_invoice_fields(invoice_fields):
    client = mistralai.Client(api_key=os.getenv("MISTRAL_API_KEY"))
    response = client.create_completion(
        model="mistral-large",
        prompt=f"Summarize the following invoice fields: {invoice_fields}",
        max_tokens=150,
    )
    return response.choices[0].text.strip()
