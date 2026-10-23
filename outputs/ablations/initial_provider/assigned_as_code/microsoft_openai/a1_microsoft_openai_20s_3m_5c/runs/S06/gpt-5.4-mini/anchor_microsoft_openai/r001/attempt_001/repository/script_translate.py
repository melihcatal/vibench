from openai import OpenAI


def script_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.responses.create(
        model='gpt-5.4-mini',
        input=[
            {'role': 'system', 'content': 'Translate narration scripts while preserving meaning and punctuation.'},
            {'role': 'user', 'content': payload['text']},
        ],
    )
    return {'text': response.output_text}
