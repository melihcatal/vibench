import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

def summarize_live_meeting_chunks(chunks: list[str]) -> str:
    context = " ".join(chunks)
    messages = [
        {"role": "system", "content": "Summarize the key points from this live meeting transcript chunk."},
        {"role": "user", "content": context}
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    return response.choices[0].message.content
