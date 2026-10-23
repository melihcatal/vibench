import os
from messaging_client import get_openai_client
from messaging_models import EventMessage

def summarize_message(message: EventMessage) -> str:
    client = get_openai_client()
    
    content_to_summarize = f"Event Type: {message.event_type}\nPayload: {message.payload}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes messages succinctly."},
            {"role": "user", "content": f"Summarize the following message content: {content_to_summarize}"}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
