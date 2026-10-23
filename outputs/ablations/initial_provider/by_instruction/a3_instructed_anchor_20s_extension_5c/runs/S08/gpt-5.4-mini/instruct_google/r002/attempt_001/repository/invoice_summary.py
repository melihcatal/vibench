from google import genai


def invoice_summary(invoice_fields: dict) -> str:
    client = genai.Client(api_key=None)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Summarize this invoice fields JSON in one paragraph.", str(invoice_fields)],
    )
    return response.text
