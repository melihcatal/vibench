import os
from mistralai.client import MistralClient

def summarize_quality(text):
    client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))
    response = client.chat(model='mistral-medium', messages=[{'role': 'user', 'content': f'Summarize the quality issues in this translation: {text}'}])
    return response.choices[0].message.content

if __name__ == '__main__':
    print(summarize_quality('The translation has some issues with grammar and vocabulary.'))