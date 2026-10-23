def format_request(prompt, max_tokens):
    return {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': max_tokens
    }

def parse_response(response):
    return response.choices[0].text.strip()