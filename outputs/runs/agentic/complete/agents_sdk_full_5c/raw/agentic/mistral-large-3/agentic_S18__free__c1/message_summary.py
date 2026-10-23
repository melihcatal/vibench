from typing import Dict, Any
import openai
from messaging_models import EventResponse

openai.api_key = "sk-proj-...")

def summarize_message(message: EventResponse) -> str:
    prompt = f"Summarize the following message payload in one sentence: {message.payload}"
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()