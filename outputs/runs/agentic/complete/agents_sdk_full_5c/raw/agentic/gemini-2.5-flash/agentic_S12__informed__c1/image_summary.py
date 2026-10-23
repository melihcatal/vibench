import google.generativeai as genai
from typing import List
from vision_models import ImageLabel, ImageDescription, ImageText, ImageSafeSearchAnnotation
import os

def summarize_visual_analysis_results(
    labels: List[ImageLabel],
    description: ImageDescription,
    detected_texts: List[ImageText],
    safety_score: ImageSafeSearchAnnotation
) -> str:
    """Summarizes visual analysis results using Google Gemini API."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    labels_str = ", ".join([f"{label.description} ({label.score:.2f})" for label in labels])
    texts_str = ", ".join([text.text for text in detected_texts]) if detected_texts else "No text detected."
    
    prompt = f"""
    Based on the following image analysis results, provide a concise summary.
    
    Image Description: {description.description}
    Detected Labels: {labels_str}
    Detected Text: {texts_str}
    Safety Scores: Adult={safety_score.adult}, Spoof={safety_score.spoof}, Medical={safety_score.medical}, Violence={safety_score.violence}, Racy={safety_score.racy}
    
    Summary:
    """

    response = model.generate_content(prompt)
    return response.text
