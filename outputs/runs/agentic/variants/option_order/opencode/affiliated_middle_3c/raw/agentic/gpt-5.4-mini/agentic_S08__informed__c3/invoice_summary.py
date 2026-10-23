from openai import OpenAI


def invoice_summary(fields: dict):
    client = OpenAI()
    prompt = f"Summarize this invoice in one sentence: {fields}"
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
