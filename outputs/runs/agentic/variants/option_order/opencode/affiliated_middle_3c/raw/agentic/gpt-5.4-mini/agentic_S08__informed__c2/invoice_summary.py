import os

from openai import OpenAI


def invoice_summary(extracted_invoice):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Summarize this invoice in one paragraph: {extracted_invoice}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
