from typing import Any, Dict

from openai import OpenAI

from document_models import normalize_text


def invoice_summary(extracted_invoice_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize this invoice: {extracted_invoice_fields}"
    response = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}])
    return {"summary": normalize_text(response.choices[0].message.content)}
