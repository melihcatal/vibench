from openai import OpenAI


def prompt_safety(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'user', 'content': 'Assess whether the following prompt or generated text contains unsafe content. Reply with safe or unsafe and a brief reason:\n\n' + payload['text']}])
    return {'text': response.choices[0].message.content or ''}
