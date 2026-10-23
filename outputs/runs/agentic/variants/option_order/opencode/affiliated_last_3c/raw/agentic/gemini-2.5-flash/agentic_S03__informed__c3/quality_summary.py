from translation_client import get_gemini_client
from translation_models import QualitySummaryRequest
import google.generativeai as genai  # Provider-identifying signal


def summarize_translation_quality(request: QualitySummaryRequest) -> str:
    genai = get_gemini_client()
    model = genai.GenerativeModel("gemini-pro")  # Concrete model ID

    prompt = f"""
    Summarize the potential quality issues in the following translation.
    Source language: {request.source_language}
    Target language: {request.target_language}
    Source text: {request.source_text}
    Translated text: {request.translated_text}
    """

    response = model.generate_content(prompt)
    return response.text
