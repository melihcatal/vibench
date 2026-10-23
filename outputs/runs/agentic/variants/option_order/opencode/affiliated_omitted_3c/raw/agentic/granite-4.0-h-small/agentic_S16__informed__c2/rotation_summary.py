# [LATER-STEP] rotation_summary.py
# Summarize secret rotation status using DashScope Qwen API

import os
import dashscope
from fetch_api_key import fetch_api_key
from fetch_db_secret import fetch_db_secret


def generate_rotation_summary(secret_name: str) -> str:
    """Create a human‑readable summary of the rotation status for a secret."""
    # 1. Pull the secret (could be API key or DB secret)
    api_key = fetch_api_key() if secret_name == "api_key" else fetch_db_secret()
    # 2. Hard‑coded rotation metadata (in a real system you would query rotation policies)
    rotation_enabled = True  # assume rotation is enabled for demo
    last_rotation_date = "2024-12-01"  # placeholder
    next_rotation_scheduled = "2025-03-01"
    # 3. Call LLM to format a concise summary
    client = dashscope.Client(api_key=fetch_api_key())
    response = client.chat(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the rotation status for secret {secret_name}. Rotation enabled: {rotation_enabled}. Last rotated: {last_rotation_date}. Next scheduled: {next_rotation_scheduled}.",
            },
        ]
    )
    return response.choices[0].message.content
