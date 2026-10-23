import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def archive_summary(transcript):
    client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])
    messages = [
        ChatMessage(
            role="user", content=f"Summarize the following transcript: {transcript}"
        )
    ]
    chat_response = client.chat(model="mistral-medium", messages=messages)
    return chat_response.choices[0].message.content
