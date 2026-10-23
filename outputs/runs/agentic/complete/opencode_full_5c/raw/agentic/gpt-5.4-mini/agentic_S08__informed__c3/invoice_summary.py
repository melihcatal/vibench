from openai import OpenAI
from document_models import normalize_expense_payload

def invoice_summary(request):
    payload = normalize_expense_payload(request)
    client = OpenAI(api_key=None)
    text = payload.get('text') or str(payload)
    resp = client.chat.completions.create(model='gpt-4.1-mini', messages=[{'role': 'system', 'content': 'Summarize invoice fields.'}, {'role': 'user', 'content': text}])
    return {'provider': 'openai', 'model': 'gpt-4.1-mini', 'summary': resp.choices[0].message.content}
