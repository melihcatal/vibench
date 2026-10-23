from openai import OpenAI


def invoice_summary(invoice_fields):
    client = OpenAI()
    prompt = f"Summarize this invoice in one paragraph: {invoice_fields}"
    result = client.responses.create(model="gpt-4.1-mini", input=prompt, temperature=0.2)
    return result.output_text
