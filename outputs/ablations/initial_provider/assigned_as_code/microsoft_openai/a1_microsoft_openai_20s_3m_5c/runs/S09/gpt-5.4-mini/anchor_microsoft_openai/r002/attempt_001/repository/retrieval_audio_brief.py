from openai import OpenAI


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.responses.create(model='gpt-5.4-mini', input=payload['results'])
    return {'brief_text': response.output_text}
