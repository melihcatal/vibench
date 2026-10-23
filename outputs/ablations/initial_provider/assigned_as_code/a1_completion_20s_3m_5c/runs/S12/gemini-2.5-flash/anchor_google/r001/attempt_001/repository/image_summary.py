import google.generativeai as genai
import os
from vision_models import DetectedLabels, ImageDescription, DetectedText, ImageModerationResult

def image_summary(analysis_results: dict, config: dict = None) -> dict:
    config = config or {}
    
    # Configure the API key for Google Generative AI
    # It's recommended to set GOOGLE_API_KEY as an environment variable
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    # Extract relevant information from analysis_results
    labels = analysis_results.get("labels", DetectedLabels()).labels
    description = analysis_results.get("description", ImageDescription(description="", confidence=0.0)).description
    detected_text = analysis_results.get("detected_text", DetectedText()).texts
    safety_scores = analysis_results.get("safety_scores", ImageModerationResult()).safe_search_annotation

    prompt = """
    Summarize the following image analysis results in a concise paragraph. 
    Focus on key visual elements, detected text, and any safety concerns. 
    
    Labels: {}
    Description: {}
    Detected Text: {}
    Safety Scores: {}
    """.format(
        ", ".join([f"{label.description} (confidence: {label.score:.2f})" for label in labels]),
        description,
        ", ".join([text.text for text in detected_text]),
        f"Adult: {safety_scores.adult}, Spoof: {safety_scores.spoof}, Medical: {safety_scores.medical}, Violence: {safety_scores.violence}, Racy: {safety_scores.racy}" if safety_scores else "N/A"
    )

    try:
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except Exception as e:
        raise RuntimeError(f"Error generating summary: {e}")
