from openai import OpenAI


def invoice_summary(extracted_invoice: dict) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in one sentence: {extracted_invoice}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return getattr(response, "output_text", "")
