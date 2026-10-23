from mistralai.client import MistralClient
import os

def summarize_rotation_status(rotation_status: str) -> str:
    client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))
    messages = [
        {
            'role': 'user',
            'content': f'Summarize the following secret rotation status in a concise bullet point list:\\n{rotation_status}'
        }
    ]
    response = client.chat(
        model='mistral-large-latest',
        messages=messages
    )
    return response.choices[0].message.content
