from openai import OpenAI


def spoken_brief(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'user', 'content': 'Rewrite the following model output as a short spoken brief that sounds natural when read aloud:\n\n' + payload['text']}])
    return {'text': response.choices[0].message.content or ''}
