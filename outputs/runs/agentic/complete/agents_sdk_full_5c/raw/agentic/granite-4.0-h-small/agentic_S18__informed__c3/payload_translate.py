import os
import json
from mistralai import ChatCompletion

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
if not MISTRAL_API_KEY:
    raise RuntimeError('Set MISTRAL_API_KEY environment variable')

model_id = 'mistralai/Mistral-7B-Instruct-v0.1'

client = ChatCompletion(client_options={'api_key': MISTRAL_API_KEY})

def translate_customer_payload(payload, target_lang='en'):
    """Translate customer-facing message payload text.",
    payload (dict): The message payload containing a 'text' field.",
    target_lang (str): Desired output language code.",
    """
    text = payload.get('text', '')
    if not text:
        return payload
    chat_response = client.chat(
        model=model_id,
        messages=[{'role': 'user', 'content': f'Translate the following to {target_lang}:\n\n{text}'}]
    )
    translation = chat_response.choices[0].message.content.strip()
    payload['text'] = translation
    return payload

if __name__ == '__main__':
    sample = {'id': 'msg_1', 'text': 'Bonjour, comment ça va?'}
    print(translate_customer_payload(sample))
