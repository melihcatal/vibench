# [LATER-STEP] record_summary.py
# Summarize retrieved document records using Anthropic Claude

import os
import json
import requests

# Anthropic Claude Chat API configuration (uses environment variables)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "Anthropic-Version": "2023-06-01",
    "Content-Type": "application/json",
}


def summarize_records(records, max_tokens=150):
    """Create a concise summary of a list of document records.

    Args:
        records (list): List of dicts representing documents.
        max_tokens (int): Max tokens for the generated summary.

    Returns:
        str: Human‑readable summary text.
    """
    # Build the prompt for Claude
    prompt = "Summarize the following records in a short paragraph:\n\n"
    for idx, rec in enumerate(records, 1):
        prompt += f"Record {idx}: {json.dumps(rec, ensure_ascii=False)}\n"
    prompt += "\n"

    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(ANTHROPIC_ENDPOINT, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    return result["content"][0]["text"]


# Example usage (uncomment locally):
# records = [{'id': '1', 'title': 'Alpha', 'score': 42}, {'id': '2', 'title': 'Beta'}]
# print(summarize_records(records))
