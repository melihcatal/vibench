import os
from typing import Dict, Any
import google.generativeai as genai
from translation_models import QualitySummaryRequest, QualitySummaryResponse

def summarize_translation_quality(payload: QualitySummaryRequest, config: Dict[str, Any] = None) -> QualitySummaryResponse:
    config = config or {}

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier

    prompt = f"""Analyze the quality of the following translation. Provide a summary of any issues, potential improvements, or notable aspects. Assign a quality score between 0.0 and 1.0 (1.0 being perfect). 

    Source ({payload.source_language}): {payload.source_text}
    Translation ({payload.target_language}): {payload.translated_text}

    Respond in the following format:
    Summary: [Your summary]
    Quality Score: [Your score, e.g., 0.85]
    """

    response = model.generate_content(prompt)
    summary_text = response.text

    summary = ""
    quality_score = None

    for line in summary_text.splitlines():
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Quality Score:"):
            try:
                quality_score = float(line.replace("Quality Score:", "").strip())
            except ValueError:
                quality_score = None

    return QualitySummaryResponse(summary=summary, quality_score=quality_score)
