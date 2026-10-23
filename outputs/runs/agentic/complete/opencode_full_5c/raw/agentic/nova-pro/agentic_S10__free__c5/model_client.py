import os

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/complete"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def get_headers():
    return {
        "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
        "Content-Type": "application/json",
    }


def get_payload(prompt, max_tokens):
    return {"prompt": prompt, "max_tokens_to_sample": max_tokens}
