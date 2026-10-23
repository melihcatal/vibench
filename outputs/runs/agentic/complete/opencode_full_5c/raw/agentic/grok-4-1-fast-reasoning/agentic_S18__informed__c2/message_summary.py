import os
import json
from openai import OpenAI
from messaging_models import MessageEvent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_message_processing(event: MessageEvent) -> str:
    payload_str = json.dumps(event.payload)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this message concisely: {payload_str}",
            }
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()
