import os
import openai
from typing import List
from safety_models import ModerationResult

def summarize_moderation_decisions(decisions: List[ModerationResult]) -> str:
    """
    Uses OpenAI's GPT model to generate a human-readable summary of moderation decisions.

    Args:
        decisions: A list of ModerationResult objects.

    Returns:
        A summary string.
    """
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    except TypeError:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
    
    if not decisions:
        return "No moderation decisions to summarize."

    # Prepare the input for the model
    decision_lines = []
    for d in decisions:
        failed_categories = [
            f"{cat.category} (Severity: {cat.severity})"
            for cat in d.categories if not d.passed
        ]
        status = "FLAGGED" if not d.passed else "PASSED"
        reason = ", ".join(failed_categories) if failed_categories else "N/A"
        text_preview = d.text[:50] + "..." if len(d.text) > 50 else d.text
        decision_lines.append(f"- Text: '{text_preview}', Status: {status}, Reason: {reason}")

    prompt = (
        "You are a moderation analyst's assistant. "
        "Summarize the following list of content moderation decisions into a brief, "
        "clear report. Highlight any trends, such as common violation categories.\n\n"
        "Decisions:\n"
        f"{'\n'.join(decision_lines)}\n\n"
        "Summary:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Failed to generate summary."
