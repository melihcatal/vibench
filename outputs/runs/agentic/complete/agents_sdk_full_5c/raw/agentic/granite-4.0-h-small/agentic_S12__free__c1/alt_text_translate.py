import requests, json, os

def alt_text_translate(description, target_lang='es'):
    """Translate image description using OpenAI's translation endpoint (or any provider).
    This example assumes a provider that offers a /v1/chat/completions style translation.",
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('Missing OPENAI_API_KEY environment variable')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    prompt = f'Translate the following English caption to {target_lang} without extra commentary:\n\n""" + description + '"""'
    payload = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    translated = data['choices'][0]['message']['content'].strip()
    return translated
