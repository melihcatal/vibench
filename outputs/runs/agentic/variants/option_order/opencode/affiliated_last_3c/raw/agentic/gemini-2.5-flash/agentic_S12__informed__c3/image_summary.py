import os
import google.generativeai as genai
from typing import List, Dict, Any


class SummaryRequest:
    def __init__(self, analysis_results: Dict[str, Any]):
        self.analysis_results = analysis_results


class SummaryResponse:
    def __init__(self, summary_text: str):
        self.summary_text = summary_text


def summarize_image_analysis(request: SummaryRequest) -> SummaryResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    analysis_text = """Image Analysis Results:
Labels: {labels}
Description: {description}
Detected Text: {text}
Safety Annotations: {safety}
""".format(
        labels=request.analysis_results.get("labels", "N/A"),
        description=request.analysis_results.get("description", "N/A"),
        text=request.analysis_results.get("text", "N/A"),
        safety=request.analysis_results.get("safety", "N/A"),
    )

    prompt = f"""Summarize the following image analysis results in a concise paragraph:

{analysis_text}
"""

    response = model.generate_content(prompt)
    summary = response.text
    return SummaryResponse(summary_text=summary)
