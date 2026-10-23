import os
from typing import Dict, Any, List
import google.generativeai as genai

def image_summary(analysis_results: Dict[str, Any]) -> Dict[str, str]:
    """
    Summarizes visual analysis results using Google's Gemini Pro model.

    Args:
        analysis_results: A dictionary containing various analysis results
                          (e.g., labels, description, detected text, safety scores).

    Returns:
        A dictionary containing the summarized text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt_parts = [
        "Summarize the following image analysis results:",
        "Labels: " + ", ".join([label['Name'] for label in analysis_results.get('labels', [])]),
        "Description: " + analysis_results.get('description', ''),
        "Detected Text: " + ", ".join([text['Text'] for text in analysis_results.get('detected_text', [])]),
        "Safety Labels: " + ", ".join([label['Name'] for label in analysis_results.get('safety_labels', [])]),
        "Provide a concise summary of the image content and any notable safety concerns or detected text."
    ]

    response = model.generate_content("\n".join(prompt_parts))
    
    return {"summary": response.text}
