from typing import Dict, Any
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from vertexai.generative_models import GenerationConfig
import os

def summarize_visual_analysis_results(analysis_results: Dict[str, Any], original_image_bytes: bytes) -> str:
    """
    Summarizes visual analysis results using a generative AI model (Google Vertex AI Gemini).
    """
    # Ensure GOOGLE_CLOUD_PROJECT is set for Vertex AI initialization
    # If you run this locally, make sure `gcloud auth application-default login` is done.
    # The model used here is 'gemini-pro-vision' for multimodal input.
    # It takes text and image as input.

    # Placeholder for actual Vertex AI initialization if not globally configured.
    # import vertexai
    # vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1") # Example location

    model = GenerativeModel("gemini-pro-vision")

    # Construct the prompt with analysis results
    prompt_parts = [
        "Summarize the following visual analysis results for an image:",
        f"Detected Labels: {', '.join(analysis_results.get('labels', []))}",
        f"Description: {analysis_results.get('description', '')}",
        f"Detected Text: {analysis_results.get('detected_text', '')}",
        f"Safety Scores: {analysis_results.get('safety_scores', {})}",
        "Provide a concise summary focusing on the key visual elements and any notable aspects like text or safety concerns."
    ]

    # Add the original image to the prompt for multimodal summarization
    image_part = Image.from_bytes(original_image_bytes)
    contents = [image_part] + [Part.from_text(part) for part in prompt_parts]

    # Configure generation to get a concise summary
    generation_config = GenerationConfig(
        max_output_tokens=200,
        temperature=0.2,
        top_p=0.8,
    )

    try:
        response = model.generate_content(contents, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"Error summarizing with Gemini: {e}")
        # Fallback to a simpler text-only summary if multimodal fails
        text_summary = f"Summary: Labels: {', '.join(analysis_results.get('labels', []))}. " \
                       f"Description: {analysis_results.get('description', '')}. " \
                       f"Text: {analysis_results.get('detected_text', '')}. " \
                       f"Safety: {analysis_results.get('safety_scores', {})}. "
        return text_summary
