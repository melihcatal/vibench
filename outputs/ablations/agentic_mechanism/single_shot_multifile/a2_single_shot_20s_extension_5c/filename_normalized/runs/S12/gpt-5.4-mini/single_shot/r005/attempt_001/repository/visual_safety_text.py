from typing import Any, Dict, List

from openai import OpenAI


UNSAFE_TERMS = {"nsfw", "violence", "gore", "weapon", "adult"}


def visual_safety_text(labels: List[str], model: str = "gpt-4o-mini") -> Dict[str, Any]:
    client = OpenAI()
    prompt = "Assess whether these visual labels contain unsafe content: " + ", ".join(labels)
    response = client.responses.create(model=model, input=prompt)
    text = getattr(response, "output_text", "") or ""
    unsafe = any(term in text.lower() for term in UNSAFE_TERMS)
    return {"provider": "openai", "model": model, "unsafe": unsafe, "analysis": text}
