from openai import OpenAI

client = OpenAI()
MODEL = 'gpt-4o-mini'


def appeal_translate(text, target_language='en'):
    prompt = f'Translate this moderation appeal into {target_language}: {text}'
    response = client.chat.completions.create(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response.choices[0].message.content
