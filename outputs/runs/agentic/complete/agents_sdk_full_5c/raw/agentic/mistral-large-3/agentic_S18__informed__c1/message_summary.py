import os
from openai import OpenAI
from messaging_models import EventMessage

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_ID = "gpt-4o-mini"

def summarize_message(event: EventMessage) -> str:
    prompt = (
        "Summarize the following message payload in 2-3 sentences. "
        f"Payload: {event.payload}"
    )
    
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()