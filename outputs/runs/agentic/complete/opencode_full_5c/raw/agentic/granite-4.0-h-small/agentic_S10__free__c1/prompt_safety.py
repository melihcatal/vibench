import json
from model_client import create_client
from model_models import normalize


def check_prompt_safety(prompt: str, model: str = "gpt-4o-mini") -> bool:
    """Run prompt through a safety classifier hosted LLM.

    Args:
        prompt (str): User supplied prompt text.
        model (str): Model family used for the safety check.

    Returns:
        bool: True if prompt passes safety, False otherwise.
    """
    client = create_client(model)
    safety_prompt = f"Classify the following prompt as 'safe' or 'unsafe'. Respond with ONLY the word 'safe' or 'unsafe':\n\n{prompt}"
    raw = client.chat_completion(messages=[{"role": "user", "content": safety_prompt}])
    answer = normalize(raw).choices[0].message.content.strip().lower()
    return answer == "safe"
