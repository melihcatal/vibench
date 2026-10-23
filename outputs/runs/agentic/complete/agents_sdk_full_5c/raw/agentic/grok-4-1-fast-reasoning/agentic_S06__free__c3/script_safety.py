import os
from openai import OpenAI
from typing import Any

def check_safety(script: str) -> dict[str, Any]:
    """Check narration scripts for unsafe content."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=script)
    return response.results[0]
