from openai import OpenAI


def invoice_summary(extracted_invoice):
    client = OpenAI()
    prompt = f"Summarize this invoice in one sentence: {extracted_invoice}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
