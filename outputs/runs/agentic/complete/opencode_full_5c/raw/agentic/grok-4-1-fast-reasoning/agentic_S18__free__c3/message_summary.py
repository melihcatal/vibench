import os
import json
from typing import List
from openai import OpenAI
from messaging_models import PubSubMessage


def summarize_messages(messages: List[PubSubMessage]) -> str:
    if not messages:
        return "No messages to summarize."
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    texts = []
    for m in messages[:10]:
        payload_str = json.dumps(m.payload)[:1000]
        texts.append(payload_str)
    prompt = (
        f"Summarize the key points from these message payloads:\\n\\n{{texts}}".format(
            texts="\\n\\n".join(texts)
        )
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content
