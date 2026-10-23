# [LATER-STEP] onboarding_summary.py
# Summarize onboarding state for support using OpenAI embeddings & GPT
import os
import openai
import uuid
from datetime import datetime

# Provider identification: OpenAI Chat Completion (GPT-4o)
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

ONBOARDING_NOTES_COLLECTION = "onboarding_notes"  # placeholder collection name


def summarize_onboarding(user_id: str, notes: list) -> str:
    """Generate a concise support summary of onboarding state."""
    # Simple prompt template
    prompt = f"You are a support agent. Summarize the onboarding progress for user {user_id}. Provide a brief overview of completed steps and any pending issues. Use the following notes as context:\n\n{'\n'.join(notes)}\n\nReturn ONLY the summary, no extra commentary."
    response = openai.ChatCompletion.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
