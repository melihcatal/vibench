from openai import OpenAI


def script_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['api_key'])
    response = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[
            {'role': 'system', 'content': 'Translate narration scripts accurately.'},
            {'role': 'user', 'content': payload['text']},
        ],
    )
    return {'text': response.choices[0].message.content}
