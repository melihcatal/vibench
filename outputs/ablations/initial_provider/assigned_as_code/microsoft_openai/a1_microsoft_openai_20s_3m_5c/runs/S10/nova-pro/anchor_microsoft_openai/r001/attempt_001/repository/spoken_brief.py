from.model_client import get_client

def generate_spoken_brief(payload, config=None):
    client = get_client(config)
    response = client.chat.completions.create(model='gpt-5.4-mini',
        messages=[{'role': 'user', 'content': 'Generate a spoken brief from the following text:

' + payload['text']}])
    return {'spoken_brief': response.choices[0].message.content or ''}