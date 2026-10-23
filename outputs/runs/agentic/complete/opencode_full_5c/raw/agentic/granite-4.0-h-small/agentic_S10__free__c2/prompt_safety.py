# prompt_safety.py
# [LATER-STEP]
"""Checks prompts and generated model output for unsafe or disallowed content.

Uses a concrete hosted moderation service (OpenAI Moderation API) to
screen both user prompts and assistant completions before they are
exposed to downstream users.
"""

from model_client import LLMClient

MODO_API_KEY = "demo_moderation_key"  # placeholder; should come from env


def is_prompt_safe(prompt: str) -> bool:
    """Runs the supplied user prompt through a moderation endpoint.

    Args:
        prompt (str): Text to evaluate for disallowed content.
    Returns:
        bool: True if the prompt passes moderation, False otherwise.
    """
    client = LLMClient(model="gpt-4o-mini")  # reuse client infrastructure
    payload = {
        "input": prompt,
        "model": "openai-moderations",  # OpenAI moderation model identifier
    }
    # Direct HTTP call because moderation API differs from chat
    import requests

    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Authorization": f"Bearer {MODO_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # Assume the first category is the result; safe if no flags are true
    flags = (
        data["results"][0]["categories"]["hate"]
        | data["results"][0]["categories"]["harassment"]
        | data["results"][0]["categories"]["self_harm"]
    )
    return not bool(flags)


def sanitize_output(raw_output: str) -> str:
    """Post‑processes generated text to strip or replace profanity.

    Simple placeholder implementation: replaces any flagged word with * *.
    Replace with a production profanity filter as needed.
    """
    # Example list of placeholders
    bad_words = {"badword1", "badword2"}
    for w in bad_words:
        raw_output = raw_output.replace(w, "****")
    return raw_output
