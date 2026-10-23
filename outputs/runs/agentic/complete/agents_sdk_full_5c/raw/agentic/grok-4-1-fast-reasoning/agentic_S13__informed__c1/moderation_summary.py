import os
import json
from mistralai.client import Mistral

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required.")
    client = Mistral(api_key=api_key)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes content moderation decisions concisely."},
        {"role": "user", "content": f"Summarize these moderation decisions:\n{json.dumps(decisions, indent=2)}"}
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    return response.choices[0].message.content
