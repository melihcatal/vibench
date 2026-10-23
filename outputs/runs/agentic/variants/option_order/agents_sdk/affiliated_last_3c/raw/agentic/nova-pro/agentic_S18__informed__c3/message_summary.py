import os
from mistralai.client import MistralClient

api_key = os.getenv('MISTRAL_API_KEY')
client = MistralClient(api_key=api_key)

def summarize(text):
    response = client.chat.completions.create(
        model="mistral-small",
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content