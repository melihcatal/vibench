import os
import mistralai

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def moderation_summary(text):
    client = mistralai.Client(api_key=MISTRAL_API_KEY)
    response = client.chat.completions.create(
        model='mistral-medium',
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content