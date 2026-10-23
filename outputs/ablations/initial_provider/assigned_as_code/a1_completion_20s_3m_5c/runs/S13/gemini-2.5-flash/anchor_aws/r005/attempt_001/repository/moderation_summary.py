import os
from typing import Dict, Any
from anthropic import Anthropic

def summarize_moderation_decisions(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=anthropic_api_key)

    moderation_decisions = payload["moderation_decisions"]
    summary_prompt = f"""
    Summarize the following moderation decisions. Highlight key reasons for any unsafe classifications and provide an overall sentiment.

    Moderation Decisions:
    {moderation_decisions}
    """

    model_name = config.get("anthropic_model", "claude-3-opus-20240229") # Using a specific Claude model

    response = client.messages.create(
        model=model_name,
        max_tokens=config.get("max_tokens", 200),
        messages=[
            {"role": "user", "content": summary_prompt}
        ]
    )

    summary = response.content[0].text

    return {"summary": summary}
