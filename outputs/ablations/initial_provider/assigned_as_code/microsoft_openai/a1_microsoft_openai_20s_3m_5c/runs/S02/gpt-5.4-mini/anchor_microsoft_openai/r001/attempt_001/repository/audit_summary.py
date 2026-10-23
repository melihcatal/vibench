from openai import OpenAI


def audit_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('openai_api_key'))
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=payload.get('events', []),
    )
    return {'summary': response.output_text}
