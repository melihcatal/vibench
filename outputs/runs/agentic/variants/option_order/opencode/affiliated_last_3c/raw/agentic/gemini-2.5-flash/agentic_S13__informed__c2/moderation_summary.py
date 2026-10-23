import os
import google.generativeai as genai
from typing import List, Dict, Any
from safety_models import TextModerationResponse, ModerationCategory


def summarize_moderation_decisions(
    texts: List[str], moderation_responses: List[TextModerationResponse]
) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    summary_prompt = """Summarize the moderation decisions for the following texts. For each text, indicate if it was flagged and for which categories, and provide a brief summary of the content's potential safety issues. Also provide an overall summary of the moderation batch.

"""

    for i, (text, response) in enumerate(zip(texts, moderation_responses)):
        summary_prompt += f"Text {i + 1}: '{text}'\n"
        flagged_categories = []
        for cat_analysis in response.categories_analysis:
            # Assuming a severity greater than 0 means it was flagged.
            if cat_analysis.get("score", 0.0) > 0:
                flagged_categories.append(cat_analysis.get("category"))

        if flagged_categories:
            summary_prompt += f"Flagged for: {', '.join(flagged_categories)}. "
            summary_prompt += (
                f"Hate: {response.get_category_score(ModerationCategory.HATE)}, "
            )
            summary_prompt += (
                f"Sexual: {response.get_category_score(ModerationCategory.SEXUAL)}, "
            )
            summary_prompt += f"Violence: {response.get_category_score(ModerationCategory.VIOLENCE)}, "
            summary_prompt += f"SelfHarm: {response.get_category_score(ModerationCategory.SELF_HARM)}.\n"
        else:
            summary_prompt += "Not flagged.\n"

    response = model.generate_content(summary_prompt)
    return response.text
