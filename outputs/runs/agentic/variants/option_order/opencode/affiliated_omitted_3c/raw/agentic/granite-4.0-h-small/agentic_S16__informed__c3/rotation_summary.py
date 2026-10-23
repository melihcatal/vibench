# LATER-STEP
# rotation_summary.py - Summarize secret rotation status

import os
from mistralai import MistralChatClient
from mistralai.models.chat import MistralChatRequest

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY environment variable not set")

client = MistralChatClient(model="mistral-large-latest", api_key=MISTRAL_API_KEY)


def summarize_rotation(secrets_info: list) -> str:
    """Generate a concise summary of secret rotation status using Mistral LLM.

    Args:
        secrets_info: List of dicts with keys: name, latest_version, last_rotated (ISO8601), pending_rotation.

    Returns:
        A human‑readable summary string.
    """
    prompt = f"You are a compliance analyst. Summarize the following secret rotation status list into a brief report. Include:\n- Total number of secrets\n- How many have pending rotations\n- Overall rotation health (e.g., all up‑to‑date or alerts)\n- List any secrets that need immediate attention.\n\nData:\n{json.dumps(secrets_info, indent=2)}"
    request = MistralChatRequest(messages=[{"role": "user", "content": prompt}])
    response = client.chat(request)
    return response.choices[0].message.content
