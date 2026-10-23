from openai import OpenAI


def invoice_summary(invoice_fields: dict) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice in one sentence: {invoice_fields}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
