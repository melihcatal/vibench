import os
from typing import List, Dict, Any
from openai import OpenAI
from safety_models import SummaryResult

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> SummaryResult:
    """
    Uses an OpenAI model to summarize a list of moderation decisions.

    :param decisions: A list of moderation decision dictionaries.
    :return: A SummaryResult containing the summary text.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    decision_str = "\n".join([str(d) for d in decisions])
    
    prompt = f"""
    The following is a list of content moderation decisions in JSON format.
    Please provide a brief, high-level summary of these events.
    Focus on the number of violations, the most common categories,
    and any notable patterns.

    Decisions:
    {decision_str}

    Summary:
    """
    
    model_name = "gpt-4o-mini"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for content moderation teams."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content or "No summary generated."
    except Exception as e:
        summary = f"Could not generate summary: {e}"

    return SummaryResult(summary=summary.strip(), model_used=model_name)
