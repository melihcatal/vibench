import os
import json
from ibm_watsonx_ai import WatsonxGuardrails


def check_text_safety(text: str) -> dict:
    """Run IBM watsonx guardrails to detect unsafe content in a user‑provided field.

    Returns a dictionary with flags (e.g., toxic, hateful) and a safety verdict.
    """
    client = WatsonxGuardrails(
        project_id=os.getenv("WATSONX_PROJECT_ID"), api_key=os.getenv("WATSONX_API_KEY")
    )
    # The guardrails service accepts raw text; you could also pass language or category tags.
    result = client.analyze(
        text=text, categories=["toxicity", "hate_speech", "sexual_content"]
    )
    return result.to_dict()
