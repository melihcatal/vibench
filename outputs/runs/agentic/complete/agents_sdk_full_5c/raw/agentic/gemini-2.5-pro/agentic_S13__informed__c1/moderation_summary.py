import os
from typing import List, Dict, Any
from openai import OpenAI

def summarize_moderations(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of moderation decisions using an LLM.

    Args:
        decisions: A list of moderation decision dictionaries.

    Returns:
        A concise summary of the moderation actions.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if not decisions:
        return "No moderation decisions to summarize."

    # Convert decisions to a string format for the prompt
    decisions_str = "\n".join([f"- {str(d)}" for d in decisions])

    prompt = f"""
    You are a Trust and Safety analyst. Please provide a brief, high-level summary 
    of the following moderation decisions. Focus on trends, common categories of 
    violations, and any notable patterns.

    Moderation Decisions:
    {decisions_str}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for summarizing moderation data."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=200,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred while calling OpenAI API: {e}")
        return "Failed to generate summary due to an API error."
