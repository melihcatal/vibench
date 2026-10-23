from openai import OpenAI

def invoice_note_translate(request):
    payload = request if isinstance(request, dict) else getattr(request, '__dict__', {})
    client = OpenAI(api_key=None)
    text = payload.get('text') or payload.get('note') or ''
    target = payload.get('target_language') or 'en'
    resp = client.chat.completions.create(model='gpt-4.1-mini', messages=[{'role': 'system', 'content': f'Translate to {target}.'}, {'role': 'user', 'content': text}])
    return {'provider': 'openai', 'model': 'gpt-4.1-mini', 'translation': resp.choices[0].message.content}
