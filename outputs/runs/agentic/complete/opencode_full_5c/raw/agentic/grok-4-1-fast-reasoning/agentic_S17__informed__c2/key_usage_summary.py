import openai
import os
from typing import List, Dict, Any


def summarize_key_usage(events: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    events_str = "\n".join(str(event) for event in events)
    prompt = f"Summarize the following key usage and crypto events, highlighting patterns, anomalies, and totals:\\n\\n{events_str}\\n\\nProvide a structured summary."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content
