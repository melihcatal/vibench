import os
from google.cloud import aiplatform

def summarize_translation_quality(translated_text: str, original_text: str, source_lang: str, target_lang: str) -> str:
    # Initialize Vertex AI
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")

    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained text-bison model for summarization
    # Model ID: "text-bison" is a common choice for summarization tasks.
    model = aiplatform.language_models.TextGenerationModel.from_pretrained("text-bison")

    prompt = f"""Summarize any potential quality issues between the original text and its translation. Focus on accuracy, fluency, and cultural appropriateness.
Original ({source_lang}): {original_text}
Translated ({target_lang}): {translated_text}
Summary of quality issues:"""

    response = model.predict(prompt=prompt, max_output_tokens=500, temperature=0.2)

    return response.text.strip()
