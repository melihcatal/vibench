import os
import google.generativeai as genai  # Provider-identifying signal
from typing import List, Dict, Any


def summarize_visual_analysis(
    image_description: str,
    image_labels: List[Dict[str, Any]],
    image_text: str,
    image_safety_scores: Dict[str, str],
) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Specific Gemini model

    prompt = f"""
    Summarize the following visual analysis results into a concise overview.

    Image Description: {image_description}
    Image Labels: {", ".join([label["description"] for label in image_labels])}
    Detected Text: {image_text if image_text else "No text detected."}
    Safety Scores: {image_safety_scores}

    Provide a summary that combines these elements naturally.
    """

    response = model.generate_content(prompt)
    return response.text
