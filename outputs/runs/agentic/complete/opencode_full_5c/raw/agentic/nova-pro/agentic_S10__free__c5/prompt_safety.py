import requests

ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/complete'
ANTHROPIC_API_KEY = 'your-api-key'

def check_unsafe_content(text):
    headers = {
        'Authorization': f'Bearer {ANTHROPIC_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': f'Check if the following text contains unsafe content: {text}',
        'max_tokens_to_sample': 100
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    return response.json()['completion']

if __name__ == '__main__'):
    text = 'This is a text to check for unsafe content.'
    result = check_unsafe_content(text)
    print(result)