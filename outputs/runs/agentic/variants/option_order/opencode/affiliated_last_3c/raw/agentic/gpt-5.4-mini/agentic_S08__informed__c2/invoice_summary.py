from typing import Any, Dict
from openai import OpenAI
from document_client import require_env


def invoice_summary(extracted_invoice: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=require_env('OPENAI_API_KEY'))
    prompt = f"Summarize this invoice in one sentence: {extracted_invoice}"
    completion = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': prompt}])
    return {'summary': completion.choices[0].message.content, 'provider': 'openai', 'model': 'gpt-4o-mini'}
