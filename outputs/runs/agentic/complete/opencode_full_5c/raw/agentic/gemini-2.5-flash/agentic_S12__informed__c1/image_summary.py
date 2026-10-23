import os
import google.generativeai as genai
from vision_models import ImageAnalysisResult


def summarize_image_analysis(analysis_result: ImageAnalysisResult) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro for text summarization

    summary_parts = [f"Analysis for image: {analysis_result.image_uri}"]

    if analysis_result.labels:
        summary_parts.append(f"Detected labels: {', '.join(analysis_result.labels)}.")
    if analysis_result.description:
        summary_parts.append(f"Generated description: {analysis_result.description}")
    if analysis_result.text_annotations:
        detected_texts = [
            t["description"]
            for t in analysis_result.text_annotations
            if t["description"]
        ]
        if detected_texts:
            summary_parts.append(f"Detected text: {', '.join(detected_texts)}.")
    if analysis_result.safety_annotations:
        safety_info = ", ".join(
            [f"{k}: {v}" for k, v in analysis_result.safety_annotations.items()]
        )
        summary_parts.append(f"Safety annotations: {safety_info}.")

    prompt = (
        "Please summarize the following image analysis results concisely: "
        + " ".join(summary_parts)
    )

    response = model.generate_content(prompt)
    return response.text
