from vision_client import get_generative_model
from vision_models import normalize_summary_response

def image_summary(analysis_results: dict, config: dict = None) -> dict:
    model = get_generative_model()

    labels = analysis_results.get("labels", {}).get("labels", [])
    description = analysis_results.get("description", {}).get("description", "No description provided.")
    full_text = analysis_results.get("text_detection", {}).get("full_text", "No text detected.")
    safety_scores = analysis_results.get("safety_scores", {}).get("safety_scores", {})

    labels_str = ", ".join([label['name'] for label in labels]) if labels else "None"
    safety_str = ", ".join([f"{k}: {v}" for k, v in safety_scores.items()]) if safety_scores else "None"

    prompt = f"""Summarize the following image analysis results:
Labels: {labels_str}
Description: {description}
Detected Text: {full_text}
Safety Scores: {safety_str}

Provide a concise summary of the image based on these findings.
"""

    response = model.generate_content(prompt)
    summary_text = response.text

    return normalize_summary_response(summary_text)
