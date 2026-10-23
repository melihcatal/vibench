import os
from openai import OpenAI

def check_script_safety(script: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    response = client.moderations.create(
        input=script,
        model="text-moderation-latest"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }

def is_safe(script: str) -> bool:
    safety = check_script_safety(script)
    return not safety["flagged"]
