import os
import google.generativeai as genai
from safety_models import ModerationResult


def summarize_moderation_decisions(results: ModerationResult, prompt: str) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Use a specific model like 'gemini-pro'
    model = genai.GenerativeModel("gemini-pro")

    # Prepare the content for summarization
    # Assuming ModerationResult has a 'categories' field that can be converted to a string
    categories_str = ", ".join(
        [f"{c.category} (severity: {c.severity})" for c in results.categories]
    )
    input_content = f"Moderation Decision:\nBlocked: {results.blocked}\nCategories: {categories_str}\n\nPrompt: {prompt}"

    response = model.generate_content(input_content)

    if (
        response.candidates
        and response.candidates[0].content
        and response.candidates[0].content.parts
    ):
        return response.candidates[0].content.parts[0].text
    return ""
