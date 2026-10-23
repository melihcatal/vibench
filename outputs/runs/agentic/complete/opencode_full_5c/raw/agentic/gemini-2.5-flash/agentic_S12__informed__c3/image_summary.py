import os
import google.generativeai as genai
from vision_models import ImageAnalysisResult


def summarize_visual_analysis(analysis_result: ImageAnalysisResult) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt_parts = ["Summarize the following visual analysis results:"]

    if analysis_result.description:
        prompt_parts.append(
            f"- Overall description: {analysis_result.description.text}"
        )
    if analysis_result.labels:
        labels_text = ", ".join(
            [
                f"{label.description} (score: {label.score:.2f})"
                for label in analysis_result.labels
            ]
        )
        prompt_parts.append(f"- Detected labels: {labels_text}")
    if analysis_result.text:
        prompt_parts.append(f"- Detected text: {analysis_result.text}")
    if analysis_result.safety_scores:
        safety_text = ", ".join(
            [
                f"{score.category}: {score.score}"
                for score in analysis_result.safety_scores
            ]
        )
        prompt_parts.append(f"- Safety scores: {safety_text}")

    if len(prompt_parts) == 1:  # Only the initial summary prompt exists
        return "No visual analysis results provided for summarization."

    response = model.generate_content("\n".join(prompt_parts))
    return response.text
