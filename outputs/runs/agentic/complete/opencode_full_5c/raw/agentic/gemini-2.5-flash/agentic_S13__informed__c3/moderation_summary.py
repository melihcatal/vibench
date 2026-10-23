import os
import google.generativeai as genai
from safety_models import TextModerationResponse


def moderation_summary(moderation_responses: list[TextModerationResponse]) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for summarization

    summary_prompt = """
    Summarize the following moderation decisions. Highlight any reasons for flagging or safety concerns.

    Moderation Decisions:
    """
    for i, response in enumerate(moderation_responses):
        summary_prompt += f"\n--- Message {i + 1} ---"
        summary_prompt += f"\nOriginal Text: {response.original_text}"
        summary_prompt += f"\nIs Safe: {response.is_safe}"
        for result in response.results:
            summary_prompt += (
                f"\n  - Category: {result.category}, Severity: {result.severity}"
            )

    response = model.generate_content(summary_prompt)
    return response.text
