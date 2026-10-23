from openai import OpenAI

from document_client import require_env


def invoice_summary(extracted_invoice: dict) -> str:
    client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
    prompt = f"Summarize this invoice in one sentence: {extracted_invoice}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
