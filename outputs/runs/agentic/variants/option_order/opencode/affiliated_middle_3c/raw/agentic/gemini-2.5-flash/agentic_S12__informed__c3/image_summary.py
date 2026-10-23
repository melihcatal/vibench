import os
import google.generativeai as genai


def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """
    Summarizes visual analysis results using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following visual analysis results in a concise paragraph:

Labels: {analysis_results.get("labels")}
Description: {analysis_results.get("description")}
Text: {analysis_results.get("text")}
Safety: {analysis_results.get("safety")}
"""

    response = model.generate_content(prompt)
    return response.text
