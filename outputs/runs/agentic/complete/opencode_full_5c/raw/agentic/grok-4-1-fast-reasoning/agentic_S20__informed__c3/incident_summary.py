import os
from mistralai import Mistral
from typing import List
from observability_models import StructuredLog


def incident_summary(logs: List[StructuredLog]) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)
    log_texts = "\n".join(
        [f"[{log.level.upper()}] {log.service}: {log.message}" for log in logs]
    )
    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the incident from these logs:\n\n{log_texts}\n\nProvide a concise summary.",
            }
        ],
    )
    return chat_response.choices[0].message.content
