import os
from openai import OpenAI
from typing import List
from safety_models import ModerationResult

def summarize_moderation_decisions(decisions: List[ModerationResult]) -> str:
    """
    Summarizes a list of moderation decisions using an OpenAI model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_content = "Here is a list of moderation decisions for a batch of user-submitted content:\n\n"
    for i, decision in enumerate(decisions):
        prompt_content += f"Item {i+1}:\n"
        prompt_content += f"  - Flagged: {'Yes' if decision.flagged else 'No'}\n"
        if decision.flagged:
            flagged_categories = [
                f"{rating.category} (Severity: {rating.severity})" 
                for rating in decision.ratings if rating.severity > 0
            ]
            prompt_content += f"  - Categories: {', '.join(flagged_categories)}\n"
        prompt_content += "\n"

    prompt_content += "Please provide a brief, one-paragraph summary of these results, highlighting any trends such as the most common violation categories."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for content moderation review teams."},
                {"role": "user", "content": prompt_content}
            ]
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate a summary."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"
