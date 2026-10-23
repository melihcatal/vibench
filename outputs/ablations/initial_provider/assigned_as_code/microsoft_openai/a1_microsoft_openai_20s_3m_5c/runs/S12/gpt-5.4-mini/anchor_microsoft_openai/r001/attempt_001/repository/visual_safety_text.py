from openai import OpenAI


def visual_safety_text(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key'))
    labels = payload.get('labels', [])
    prompt = 'Assess whether the labels contain unsafe or sensitive text and return a brief verdict.'
    result = client.responses.create(model=config.get('model', 'gpt-4.1-mini'), input=[{'role': 'system', 'content': prompt}, {'role': 'user', 'content': str(labels)}])
    return {'verdict': result.output_text}
