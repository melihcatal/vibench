from openai import OpenAI


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.responses.create(model='gpt-4.1-mini', input=payload['retrieved_results'])
    return {'brief_text': response.output_text}
