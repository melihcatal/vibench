import os
from openai import OpenAI
from messaging_models import EventMessage

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_message(event: EventMessage) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the following message in one sentence."},
            {"role": "user", "content": event.data}
        ]
    )
    return response.choices[0].message.content.strip()