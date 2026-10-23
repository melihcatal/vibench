
import os
import google.generativeai as genai
from vision_models import Label, ImageDescription, DetectedText

def summarize_vision_results(
    labels: list[Label],
    description: ImageDescription,
    detected_text: list[DetectedText]
) -> str:
    """
    Summarizes visual analysis results using Google's Gemini API.
    """
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    
    # Using a specific Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Summarize the following visual analysis results into a coherent paragraph.

    Detected Labels: {', '.join([l.name for l in labels])}
    Generated Description: {description.description}
    Detected Text: {', '.join([t.text for t in detected_text])}

    Summary:
    """
    
    response = model.generate_content(prompt)
    return response.text
