import google.generativeai as genai
from typing import Dict, Any, List


def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """Summarizes visual analysis results using Google Cloud Generative AI.

    Args:
        analysis_results: A dictionary containing various analysis results
                          (e.g., labels, detected text, safety scores).

    Returns:
        A string summarizing the analysis results.
    """
    # Provider: Google Cloud Generative AI
    model = genai.GenerativeModel("gemini-pro")

    labels = analysis_results.get("labels", [])
    text_detection = analysis_results.get("text_detection", "")
    safety_scores = analysis_results.get("safety_scores", {})
    description = analysis_results.get("description", "")

    prompt_parts = [
        "Given the following visual analysis results, provide a concise summary.",
        "Visual Description: " + description,
    ]

    if labels:
        label_descriptions = [label["description"] for label in labels]
        prompt_parts.append("Detected Labels: " + ", ".join(label_descriptions))
    if text_detection:
        prompt_parts.append("Detected Text: " + text_detection)
    if safety_scores:
        safety_info = ", ".join([f"{k}: {v}" for k, v in safety_scores.items()])
        prompt_parts.append("Safety Scores: " + safety_info)

    prompt = "\n".join(prompt_parts)

    response = model.generate_content(prompt)
    return response.text
