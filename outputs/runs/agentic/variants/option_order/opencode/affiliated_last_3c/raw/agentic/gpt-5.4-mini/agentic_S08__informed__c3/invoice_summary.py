from openai import OpenAI


def summarize_invoice(fields: dict) -> str:
    client = OpenAI()
    prompt = f"Summarize this invoice concisely: {fields}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
