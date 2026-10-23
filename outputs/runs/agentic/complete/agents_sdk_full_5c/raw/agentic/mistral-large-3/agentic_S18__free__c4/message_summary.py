from openai import OpenAI
import os
from messaging_models import EventMessage

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_message(event: EventMessage) -> str:
    prompt = (
        f"Summarize the following event payload in one sentence:\n"
        f"Event Type: {event.event_type}\n"
        f"Payload: {event.payload}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()