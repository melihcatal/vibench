import os
from typing import List, Dict, Any
import anthropic

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of moderation decisions into a human-readable report.

    Args:
        decisions: A list of moderation decision dictionaries.

    Returns:
        A summary string.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment.")
        
    client = anthropic.Anthropic(api_key=api_key)

    prompt_text = "Here are the JSON results from a content moderation system. Please summarize them in a brief, human-readable paragraph, highlighting the main reasons for any flagged content.\n\n"
    for i, decision in enumerate(decisions):
        prompt_text += f"Item {i+1}: {decision}\n"

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": prompt_text,
            }
        ],
    )
    
    summary = message.content[0].text if message.content else "Could not generate summary."
    return summary
