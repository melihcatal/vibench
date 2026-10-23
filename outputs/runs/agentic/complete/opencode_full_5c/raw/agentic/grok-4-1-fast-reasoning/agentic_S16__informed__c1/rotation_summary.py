import os
import json
from typing import List
from dataclasses import asdict
from mistralai.client import MistralClient
from security_models import SecretInfo


def rotation_summary(secrets: List[SecretInfo]) -> str:
    status_data = json.dumps([asdict(s) for s in secrets])
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [
        {
            "role": "system",
            "content": "You are an expert in secret management. Summarize the rotation status concisely.",
        },
        {
            "role": "user",
            "content": f"Summarize rotation status based on this data: {status_data}",
        },
    ]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
