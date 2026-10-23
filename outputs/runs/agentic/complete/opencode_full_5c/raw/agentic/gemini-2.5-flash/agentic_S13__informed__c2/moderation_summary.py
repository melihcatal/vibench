import os
import google.generativeai as genai
from safety_models import ModerationResult


def summarize_moderation_decisions(moderation_results: list[ModerationResult]) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    summary_prompt = """Summarize the moderation decisions for the following texts. For each text, list the categories detected and their severity, and provide an overall summary of the moderation outcomes. If no categories were detected, state that.

"""

    for result in moderation_results:
        summary_prompt += f"Text: {result.text}\n"
        if result.categories:
            for category in result.categories:
                summary_prompt += f"  - Category: {category.category}, Severity: {category.severity}, Detected: {category.detected}\n"
        else:
            summary_prompt += "  No specific categories detected.\n"

    summary_prompt += "\nOverall Summary:\n"

    response = model.generate_content(summary_prompt)
    return response.text
