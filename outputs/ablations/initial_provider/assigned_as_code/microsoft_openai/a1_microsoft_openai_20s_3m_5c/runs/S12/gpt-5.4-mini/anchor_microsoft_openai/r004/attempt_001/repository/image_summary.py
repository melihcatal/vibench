from openai import OpenAI


def image_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    model = config.get('model', 'gpt-4.1-mini')
    prompt = payload.get('analysis_text') or payload.get('summary_source') or ''
    response = client.responses.create(model=model, input=[{'role': 'user', 'content': prompt}])
    return {'summary': response.output_text}
