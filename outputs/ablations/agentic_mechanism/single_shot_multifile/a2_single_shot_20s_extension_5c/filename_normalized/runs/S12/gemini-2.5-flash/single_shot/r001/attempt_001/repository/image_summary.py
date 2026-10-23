import os
from google.cloud import aiplatform
from vision_client import get_vertex_ai_text_model
from vision_models import ImageAnalysisResults, LabelResult, TextResult, SafeSearchResult, ImageDescriptionResult
from typing import List

def summarize_visual_analysis_results(analysis_results: ImageAnalysisResults) -> str:
    """
    Summarizes visual analysis results using a Google Cloud Vertex AI large language model (text-bison).
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = "text-bison@001" # Concrete model identifier

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    model = get_vertex_ai_text_model(project_id, location, model_name)

    # Construct the prompt from the analysis results
    prompt_parts = ["Please summarize the following image analysis results:\n"]

    if analysis_results.description:
        prompt_parts.append(f"Image Description: {analysis_results.description.description}\n")
    if analysis_results.labels:
        labels_text = ", ".join([f"{l.description} (score: {l.score:.2f})" for l in analysis_results.labels])
        prompt_parts.append(f"Detected Labels: {labels_text}\n")
    if analysis_results.text:
        ocr_text = " ".join([t.description for t in analysis_results.text])
        prompt_parts.append(f"Detected Text (OCR): \"{ocr_text}\"\n")
    if analysis_results.safety_scores:
        safety = analysis_results.safety_scores
        prompt_parts.append(
            f"Safety Scores: Adult: {safety.adult}, Spoof: {safety.spoof}, "
            f"Medical: {safety.medical}, Violence: {safety.violence}, Racy: {safety.racy}\n"
        )
    if analysis_results.translated_description:
        prompt_parts.append(f"Translated Description: {analysis_results.translated_description}\n")
    if analysis_results.moderation_flags:
        flags = [k for k, v in analysis_results.moderation_flags.items() if v]
        if flags:
            prompt_parts.append(f"Moderation Flags for text: {', '.join(flags)}\n")

    full_prompt = "".join(prompt_parts) + "\nProvide a concise summary."

    response = model.predict(full_prompt)
    return response.text
