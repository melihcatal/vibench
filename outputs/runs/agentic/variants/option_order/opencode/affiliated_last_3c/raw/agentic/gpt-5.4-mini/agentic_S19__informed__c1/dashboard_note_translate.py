import os
from openai import OpenAI


def dashboard_note_translate(text, target_locale, model='gpt-5.4-mini'):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f'Translate this metric or dashboard note into {target_locale}: {text}'
    resp = client.chat.completions.create(model=model, messages=[{'role': 'user', 'content': prompt}])
    return {'locale': target_locale, 'translation': resp.choices[0].message.content}
