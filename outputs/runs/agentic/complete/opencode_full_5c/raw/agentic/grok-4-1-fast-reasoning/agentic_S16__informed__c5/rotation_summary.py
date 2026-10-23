import openai
import os
import json
from typing import List
from security_models import SecretRotation


def summarize_secret_rotation_status(rotations: List[SecretRotation]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Summarize the following secret rotation statuses in a concise report, highlighting any issues, pending actions, or successes:

{json.dumps(rotations, indent=2, default=str)}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content
