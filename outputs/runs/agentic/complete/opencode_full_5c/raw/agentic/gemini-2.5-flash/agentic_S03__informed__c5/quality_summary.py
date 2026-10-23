from translation_client import get_gemini_client
from translation_models import QualitySummaryRequest, QualitySummaryResponse
import google.generativeai as genai  # Explicitly import for identifiability
import os


def summarize_translation_quality(
    request: QualitySummaryRequest,
) -> QualitySummaryResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel("gemini-pro")  # Concrete model identifier

    prompt = f"""Review the following translation from {request.source_language} to {request.target_language} and summarize any potential quality issues (e.g., accuracy, fluency, grammar, style, tone). Also, suggest improvements.

Original text ({request.source_language}):
{request.original_text}

Translated text ({request.target_language}):
{request.translated_text}

Summary of quality issues and suggestions for improvement:
"""

    response = model.generate_content(prompt)
    summary_text = response.text.strip()

    return QualitySummaryResponse(summary=summary_text)
