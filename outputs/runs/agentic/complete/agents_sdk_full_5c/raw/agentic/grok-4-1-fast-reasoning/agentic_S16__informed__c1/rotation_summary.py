import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def summarize_rotation_status(rotation_status: str) -> str:
    api_key = os.getenv('MISTRAL_API_KEY')
    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="system", content="You are an expert in secret management. Summarize the rotation status concisely."),
        ChatMessage(role="user", content=f"Summarize this secret rotation status: {rotation_status}")
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    return response.choices[0].message.content