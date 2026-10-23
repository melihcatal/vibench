from google.genai import Client


def invoice_summary(extracted: dict):
    client = Client(api_key=None)
    prompt = f"Summarize this invoice in one sentence: {extracted}"
    return client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
