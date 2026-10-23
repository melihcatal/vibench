import google.generativeai as genai
import os
from translation_models import QualitySummaryRequest

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def summarize_translation_quality(request: QualitySummaryRequest) -> str:
    model = genai.GenerativeModel("gemini-pro")
    prompt = (
        f"Summarize potential quality issues in the following translation from the original text. "
        f"Original text (inferred language): {request.source_text}\n"
        f"Translated text (to {request.target_language}): {request.translated_text}\n"
        f"Focus on accuracy, fluency, grammar, and style. Provide a concise summary."
    )
    response = model.generate_content(prompt)
    return response.text
