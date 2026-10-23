import os
from anthropic import Anthropic
from typing import List, Dict, Any

def generate_moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""
    Summarize the following moderation decisions in a concise report, highlighting patterns, counts per category, and overall safety trends:
    {decisions}
    """
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
