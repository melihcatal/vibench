import os
import google.generativeai as genai
from translation_models import QualitySummaryRequest, QualitySummaryResponse


def summarize_translation_quality(
    request: QualitySummaryRequest,
) -> QualitySummaryResponse:
    """
    Summarizes translation quality issues using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Analyze the following translation and summarize any potential quality issues,
    such as grammatical errors, awkward phrasing, mistranslations, or loss of nuance.
    Also, list specific issues found.

    Source Language: {request.source_language}
    Target Language: {request.target_language}
    Source Text: "{request.source_text}"
    Translated Text: "{request.translated_text}"

    Provide the summary and issues in a structured format.
    """

    response = model.generate_content(prompt)

    # Simple parsing, in a real scenario, more robust parsing would be needed
    # for example, guiding the LLM to output JSON.
    summary_text = response.text
    issues = [
        line.strip()
        for line in summary_text.split("\n")
        if "issue" in line.lower() or "-" in line
    ]

    return QualitySummaryResponse(summary=summary_text, issues_found=issues)
