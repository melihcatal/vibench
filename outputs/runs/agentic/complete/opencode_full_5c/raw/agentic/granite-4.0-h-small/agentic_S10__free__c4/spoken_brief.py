import os
from model_client import HostedModelClient


def generate_spoken_brief(text: str, model: str = "gpt-4o") -> str:
    """Generates a spoken-friendly brief from model output using a TTS-capable model.

    Args:
        text: Original model output.
        model: Hosted model identifier specialized for brief generation.

    Returns:
        A concise, human-readable summary suitable for speech synthesis.
    """
    client = HostedModelClient(model=model)
    prompt = f"Create a spoken brief (max 60 words) summarizing the following text:\n\n{text}"
    payload = {"prompt": prompt, "temperature": 0.2}
    response = client.chat_completion(payload)
    brief = response["choices"][0]["message"]["content"]
    return brief.strip()
