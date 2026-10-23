from openai import OpenAI


def audit_summary(payload, config=None):
    payload = dict(payload or {})
    client = OpenAI(api_key=(config or {}).get('openai_api_key'))
    events = payload.get('events', [])
    prompt = 'Summarize these federated-login audit events in concise operational language:\n' + str(events)
    response = client.responses.create(model='gpt-5.4-mini', input=prompt)
    return {'summary': response.output_text, 'model': 'gpt-5.4-mini'}
