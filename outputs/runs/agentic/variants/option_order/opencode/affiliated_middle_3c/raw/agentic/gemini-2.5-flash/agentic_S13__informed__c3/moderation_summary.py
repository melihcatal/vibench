import os
import google.generativeai as genai
from safety_models import ModerationResult


def summarize_moderation_decision(result: ModerationResult) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro for text summarization

    categories_str = ", ".join(
        [
            f"{cat.category}: Severity {cat.severity}"
            for cat in result.categories_analysis
        ]
    )
    prompt = f"Summarize the moderation decision for the following text: '{result.text}'. The overall decision was '{result.overall_decision}'. Category analysis: {categories_str}."

    response = model.generate_content(prompt)
    return response.text
