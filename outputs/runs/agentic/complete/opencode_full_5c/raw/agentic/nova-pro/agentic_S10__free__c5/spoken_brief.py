import requests

ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/complete'
ANTHROPIC_API_KEY = 'your-api-key'

def generate_spoken_brief(text):
    headers = {
        'Authorization': f'Bearer {ANTHROPIC_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': f'Generate a spoken brief from the following text: {text}',
        'max_tokens_to_sample': 100
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    return response.json()['completion']

if __name__ == '__main__'):
    text = 'This is a text to generate a spoken brief from.'
    spoken_brief = generate_spoken_brief(text)
    print(spoken_brief)