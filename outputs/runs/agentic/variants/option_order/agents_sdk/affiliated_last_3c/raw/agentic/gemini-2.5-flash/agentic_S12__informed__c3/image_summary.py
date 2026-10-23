import os
import google.generativeai as genai
from typing import Dict, Any

def summarize_visual_analysis(analysis_results: Dict[str, Any], image_context: str = "") -> str:
    """
    Summarizes visual analysis results using Google Gemini API.
    `analysis_results` could contain labels, descriptions, detected text, and safety scores.
    """
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    
    model = genai.GenerativeModel('gemini-pro')

    prompt_parts = [
        "Summarize the following visual analysis results into a concise, human-readable paragraph.",
        "Focus on key objects, actions, and any notable attributes. If safety scores are present, mention them briefly if significant.",
        f"Image context: {image_context}" if image_context else "",
        "Analysis results:",
        str(analysis_results)
    ]
    
    response = model.generate_content(" ".join(prompt_parts))
    return response.text

if __name__ == '__main__':
    # This example requires GOOGLE_API_KEY to be set.
    sample_results = {
        "labels": ["cat", "sleeping", "bed", "fur"],
        "description": "A fluffy cat is sleeping soundly on a soft bed.",
        "detected_text": [],
        "safety_scores": {"adult": 0.01, "violence": 0.005}
    }
    # summary = summarize_visual_analysis(sample_results, image_context="Pet photo album")
    # print(summary)
    pass
