import json
from model_client import ModelClient


def generate_spoken_brief(text: str, model_name: str = "gpt-4o-mini") -> str:
    """Create a concise spoken brief from model output.

    Args:
        text (str): The raw model response.
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        str: A brief, natural‑language script suitable for TTS.
    """
    client = ModelClient(model_name)
    prompt = f"Rewrite the following into a short spoken brief (≈20‑30 words) suitable for a voice assistant. Keep it natural and concise:\n\n{text}"
    brief = client.complete(prompt)
    return brief["text"].strip()
