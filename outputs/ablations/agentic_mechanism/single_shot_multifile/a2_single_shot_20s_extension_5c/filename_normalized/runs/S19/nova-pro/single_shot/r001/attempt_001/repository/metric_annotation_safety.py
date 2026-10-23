import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def check_annotation_safety(annotation):
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=f'Is the following annotation safe for public display? {annotation}',
        max_tokens=5
    )
    return 'safe' in response.choices[0].text.lower()