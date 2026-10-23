from openai import OpenAI
import os
from security_models import KeyUsageEvent

def summarize_key_usage(events: list[KeyUsageEvent]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    events_str = "\n".join([
        f"Key: {e.key_id}, Operation: {e.operation}, Bytes: {e.bytes_processed}, Time: {e.timestamp}"
        for e in events
    ])
    prompt = f"Summarize the key usage and crypto events:\n{events_str}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content