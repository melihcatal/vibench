from openai import OpenAI


def embedding_job_summary(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.responses.create(model='gpt-4.1-mini', input=payload['summary_text'])
    return {'summary': response.output_text}
