import os
import google.generativeai as genai
from typing import Dict, Any, List


def summarize_visual_analysis(
    labels: List[Dict[str, Any]],
    description: str,
    detected_text: str,
    safety_scores: Dict[str, Any],
) -> str:
    """
    Summarizes visual analysis results using the Google Gemini API.

    Args:
        labels: A list of detected labels.
        description: A generated description of the image.
        detected_text: Any text detected in the image.
        safety_scores: A dictionary of safety scores.

    Returns:
        A natural language summary of the analysis.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    prompt = f"""
    Please provide a concise, human-readable summary of the following image analysis results.
    The summary should integrate the information into a cohesive paragraph.

    Analysis Results:
    - Image Description: "{description}"
    - Detected Labels: {labels}
    - Detected Text: "{detected_text if detected_text else "None"}"
    - Safety Assessment: {safety_scores}
    
    Summary:
    """

    response = model.generate_content(prompt)
    return response.text
