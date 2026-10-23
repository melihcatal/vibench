import os
import google.generativeai as genai
from typing import Dict, Any
from vision_models import ImageAnalysisResult # Assuming vision_models.py is in the same directory

def summarize_visual_analysis(analysis_result: ImageAnalysisResult):
    """Summarizes various visual analysis results using Google's Gemini Pro model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    summary_parts = []
    if analysis_result.description:
        summary_parts.append(f"Description: {analysis_result.description}")
    if analysis_result.labels:
        summary_parts.append(f"Labels: {', '.join(analysis_result.labels)}")
    if analysis_result.detected_text:
        summary_parts.append(f"Detected Text: {analysis_result.detected_text}")
    if analysis_result.safety_scores:
        safety_info = ", ".join([f"{k}: {v}" for k, v in analysis_result.safety_scores.items()])
        summary_parts.append(f"Safety Scores: {safety_info}")

    if not summary_parts:
        return "No visual analysis data to summarize."

    full_text = "\n".join(summary_parts)
    prompt = f"Summarize the following visual analysis results concisely:\n\n{full_text}\nSummary:"

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage
    example_analysis = ImageAnalysisResult(
        image_uri="gs://example-bucket/image.jpg",
        labels=["cat", "animal", "pet"],
        description="A domestic short-haired cat with green eyes.",
        detected_text="MEOW",
        safety_scores={"adult": "VERY_UNLIKELY", "violence": "UNLIKELY", "racy": "UNLIKELY"}
    )
    print(f"Summarizing analysis for {example_analysis.image_uri}")
    summary = summarize_visual_analysis(example_analysis)
    print(f"Summary: {summary}")

    empty_analysis = ImageAnalysisResult(image_uri="gs://example-bucket/empty.jpg")
    empty_summary = summarize_visual_analysis(empty_analysis)
    print(f"Empty Analysis Summary: {empty_summary}")
