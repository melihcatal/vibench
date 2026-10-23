import os
import google.generativeai as genai
from vision_models import VisionAnalysisResult


def image_summary(analysis_result: VisionAnalysisResult) -> str:
    """
    Summarizes the visual analysis results using the Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt_parts = ["Summarize the following analysis of an image:"]

    if analysis_result.description:
        prompt_parts.append(
            f"- Primary description: {analysis_result.description.text}"
        )

    if analysis_result.labels:
        labels_str = ", ".join(
            [label.description for label in analysis_result.labels[:5]]
        )
        prompt_parts.append(f"- Detected labels: {labels_str}")

    if analysis_result.texts:
        text_str = analysis_result.texts[0].text.replace("\n", " ")
        prompt_parts.append(f"- Text found in image: '{text_str}'")

    if analysis_result.safety_ratings:
        safety_str = ", ".join(
            [f"{r.category}: {r.likelihood}" for r in analysis_result.safety_ratings]
        )
        prompt_parts.append(f"- Safety assessment: {safety_str}")

    prompt = "\n".join(prompt_parts)

    response = model.generate_content(prompt)
    return response.text
