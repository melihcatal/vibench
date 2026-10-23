import os
import google.generativeai as genai
from vision_models import ImageAnalysisResult, SummarizedImageAnalysis


def summarize_image_analysis(
    analysis_result: ImageAnalysisResult,
) -> SummarizedImageAnalysis:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following image analysis results into a concise, human-readable paragraph.
Labels: {", ".join(analysis_result.labels.labels)}
Description (best guess labels): {", ".join(analysis_result.description.best_guess_labels)}
Detected Text: {analysis_result.text.full_text}
Safety: Adult: {analysis_result.safety.adult}, Spoof: {analysis_result.safety.spoof}, Medical: {analysis_result.safety.medical}, Violence: {analysis_result.safety.violence}, Racy: {analysis_result.safety.racy}

Summary:
"""

    response = model.generate_content(prompt)
    return SummarizedImageAnalysis(summary_text=response.text)
