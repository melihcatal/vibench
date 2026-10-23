from openai import OpenAI


def invoice_summary(invoice_fields: dict) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": str(invoice_fields)}]
    )
    return response.choices[0].message.content
