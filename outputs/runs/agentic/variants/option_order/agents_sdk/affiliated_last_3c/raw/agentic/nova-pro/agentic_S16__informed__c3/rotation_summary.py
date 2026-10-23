from mistralai.client import MistralClient
import os

def summarize_rotation_status():
    client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))
    response = client.chat(model='mistral-tiny', messages=[{"role": "user", "content": "Summarize the secret rotation status."}])
    return response.choices[0].message.content