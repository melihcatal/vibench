from openai import OpenAI


def image_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key'))
    content = payload.get('analysis', {})
    prompt = 'Summarize the visual analysis results in one short paragraph.'
    result = client.responses.create(model=config.get('model', 'gpt-4.1-mini'), input=[{'role': 'system', 'content': prompt}, {'role': 'user', 'content': str(content)}])
    return {'summary': result.output_text}
