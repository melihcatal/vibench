import os
import json
from openai import OpenAI
from document_models import NormalizedExpense
from typing import Union, Dict, Any


def invoice_summary(
    normalized_expense: Union[Dict[str, Any], NormalizedExpense],
) -> str:
    client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")

    if hasattr(normalized_expense, "model_dump"):
        data = normalized_expense.model_dump()
    else:
        data = normalized_expense

    prompt = f"Provide a concise summary of this invoice in 2-3 bullet points:\\n\\n{json.dumps(data, indent=2)}"

    response = client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
