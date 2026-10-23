import os
from typing import List
import google.generativeai as genai


class QualitySummaryRequest:
    def __init__(
        self,
        original_text: str,
        translated_text: str,
        target_language: str,
        quality_criteria: List[str],
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.target_language = target_language
        self.quality_criteria = quality_criteria


class QualitySummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary


def summarize_translation_quality(
    request: QualitySummaryRequest,
) -> QualitySummaryResponse:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Review the following translation from the original text to {request.target_language}. " \
             f"Evaluate it based on the following criteria: {", ".join(request.quality_criteria)}. " \
             f"Provide a summary of any quality issues found.

Original Text: {request.original_text}
Translated Text: {request.translated_text}
Summary of Quality Issues:"""

    response = model.generate_content(prompt)
    return QualitySummaryResponse(response.text)
