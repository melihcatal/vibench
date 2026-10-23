import os
from typing import List, Dict, Any
from openai import OpenAI

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of moderation decision dictionaries into a human-readable report.
    
    Args:
        decisions: A list of raw response dictionaries from the moderation service.
    
    Returns:
        A text summary of the moderation actions.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_content = f"""
    Here is a list of moderation decisions in JSON format:
    {decisions}

    Please provide a brief, human-readable summary of these decisions. Include:
    - The total number of items processed.
    - The number of flagged items.
    - A breakdown of flags by category.
    - Any notable trends or severe violations.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for content moderation teams."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"
