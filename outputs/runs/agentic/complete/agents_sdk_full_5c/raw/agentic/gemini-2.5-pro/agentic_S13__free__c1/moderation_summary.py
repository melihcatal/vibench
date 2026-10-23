import anthropic
from safety_client import safety_clients_config
from typing import List, Dict

def summarize_moderation_decisions(decisions: List[Dict]) -> str:
    """
    Summarizes a list of moderation decisions using Anthropic's Claude.
    """
    client = anthropic.Anthropic(api_key=safety_clients_config.ANTHROPIC_API_KEY)

    decisions_str = "\n".join([f"- {d}" for d in decisions])
    
    prompt = f"""The following is a list of moderation decisions from an automated system. Please provide a brief, one-paragraph summary of the key trends. Mention the total number of items, how many were flagged, and any dominant categories of violations.

Decisions:
{decisions_str}

Summary:"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=250,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return message.content[0].text
