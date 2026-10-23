from.model_client import get_client

def translate_output(payload, config=None):
    client = get_client(config)
    response = client.chat.completions.create(model='gpt-5.4-mini',
        messages=[{'role': 'user', 'content': 'Translate the following text into ' + payload['target_language'] + ':

' + payload['text']}])
    return {'translation': response.choices[0].message.content or ''}