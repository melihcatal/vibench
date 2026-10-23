import os
from summary_llm_client import LLMClient
from typing import Dict

def summarize_onboarding(user_id: str, notes: Dict) -> str:
    """Summarize onboarding state for support staff."""
    client = LLMClient(model='gpt-4o', temperature=0)
    prompt = (
        "You are a support assistant. Provide a concise summary of a user's onboarding state."
        " Include the user ID and any onboarding notes."
    )
    context = {
        'user_id': user_id,
        'notes': notes
    }
    summary = client.chat(prompt=prompt, context=context)
    return summary
