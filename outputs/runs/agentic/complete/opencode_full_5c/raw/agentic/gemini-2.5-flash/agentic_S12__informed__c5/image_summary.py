import os
from typing import List, Dict, Any
import google.generativeai as genai  # Google Gemini API SDK import is the identifying signal
from vision_models import SummaryRequest, SummaryResult

genai.configure(
    api_key=os.environ.get("GOOGLE_API_KEY")
)  # GOOGLE_API_KEY environment variable is the identifying signal


def summarize_visual_analysis(request: SummaryRequest) -> SummaryResult:
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Gemini Pro model is the identifying signal

    # Convert the list of dictionaries to a more readable string format for the LLM
    analysis_text = "Visual Analysis Results:\n"
    for result_dict in request.analysis_results:
        for key, value in result_dict.items():
            analysis_text += f"- {key}: {value}\n"

    prompt = f"Please summarize the following visual analysis results concisely:\n\n{analysis_text}"

    response = model.generate_content(prompt)
    summary = response.text

    return SummaryResult(summary_text=summary)
