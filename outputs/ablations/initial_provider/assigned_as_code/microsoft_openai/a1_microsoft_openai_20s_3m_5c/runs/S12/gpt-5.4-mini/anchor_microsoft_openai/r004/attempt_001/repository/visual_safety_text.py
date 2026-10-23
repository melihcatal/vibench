from openai import OpenAI


def visual_safety_text(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    model = config.get('model', 'gpt-4.1-mini')
    labels = payload.get('labels', [])
    prompt = f'Identify any unsafe, sensitive, or policy-related text in these labels and return a brief judgment: {labels}'
    response = client.responses.create(model=model, input=[{'role': 'user', 'content': prompt}])
    return {'assessment': response.output_text}
