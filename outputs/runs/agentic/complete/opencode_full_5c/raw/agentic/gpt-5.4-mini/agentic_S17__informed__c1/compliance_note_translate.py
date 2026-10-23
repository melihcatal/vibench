import openai


def compliance_note_translate(text, target_language='en', api_key=None):
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'system', 'content': 'Translate compliance notes for reviewers.'}, {'role': 'user', 'content': f'Translate to {target_language}: {text}'}])
    return {'translation': response.choices[0].message.content, 'model': 'gpt-4o-mini', 'provider': 'OpenAI'}
