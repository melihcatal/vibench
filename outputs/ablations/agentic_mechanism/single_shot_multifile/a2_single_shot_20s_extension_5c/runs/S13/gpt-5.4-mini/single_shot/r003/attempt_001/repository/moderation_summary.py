from typing import Any, Dict, List

from openai import OpenAI

from safety_client import load_safety_config


def moderation_summary(decisions: List[Dict[str, Any]], language: str = "en") -> Dict[str, Any]:
    config = load_safety_config()
    client = OpenAI(api_key=config.openai_api_key)
    prompt = f"Summarize these moderation decisions in {language}: {decisions}"
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return {"summary": response.output_text, "model": "gpt-4.1-mini"}
