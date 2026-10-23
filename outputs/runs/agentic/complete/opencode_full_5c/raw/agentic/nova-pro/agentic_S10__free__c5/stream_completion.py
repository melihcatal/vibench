import requests

ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/complete'
ANTHROPIC_API_KEY = 'your-api-key'

def stream_completion(text):
    headers = {
        'Authorization': f'Bearer {ANTHROPIC_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': text,
        'max_tokens_to_sample': 100,
        'stream': True
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            print(line)

if __name__ == '__main__'):
    text = 'This is a text to stream completion.'
    stream_completion(text)