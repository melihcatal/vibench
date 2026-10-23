from openai import OpenAI


def result_translate(payload, config=None):
    config = config or {}
    target_language = payload.get('language') or 'Spanish'
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'user', 'content': 'Translate the following text into ' + target_language + ' while preserving meaning:\n\n' + payload['text']}])
    return {'text': response.choices[0].message.content or ''}
