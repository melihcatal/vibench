from openai import OpenAI
from typing import Dict, Any

from security_client import get_secrets_config

def summarize_rotation_status(rotation_logs: str) -> str:
    config = get_secrets_config()
    api_key = config['openai_api_key']
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize the secret rotation status in a few bullet points:\\n\\n{rotation_logs}"}
        ],
        max_tokens=300
    )
    return completion.choices[0].message.content