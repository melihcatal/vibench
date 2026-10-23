import os
import google.generativeai as genai
from typing import List, Dict, Any


def summarize_visual_analysis_results(analysis_results: Dict[str, Any]) -> str:
    """
    Summarize visual analysis results using the Google Gemini API.
    The GOOGLE_API_KEY environment variable must be set.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Based on the following image analysis results, provide a concise summary.
    Focus on key labels, detected text, and any safety concerns.

    Analysis Results:
    {analysis_results}

    Summary:
    """

    response = model.generate_content(prompt)
    return response.text
