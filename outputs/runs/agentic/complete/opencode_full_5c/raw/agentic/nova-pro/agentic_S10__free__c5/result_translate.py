import requests

ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/complete'
ANTHROPIC_API_KEY = 'your-api-key'

def translate_text(text, target_language):
    headers = {
        'Authorization': f'Bearer {ANTHROPIC_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': f'Translate the following text to {target_language}: {text}',
        'max_tokens_to_sample': 100
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    return response.json()['completion']

if __name__ == '__main__'):
    text = 'This is a text to translate.'
    target_language = 'Spanish'
    translated_text = translate_text(text, target_language)
    print(translated_text)