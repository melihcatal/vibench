import os
from google.cloud import aiplatform

def quality_summary(translated_text: str, original_text: str, config: dict = None) -> str:
    config = config or {}
    project_id = config.get('project_id') or os.getenv('GOOGLE_CLOUD_PROJECT')
    location = config.get('location', 'us-central1') # Vertex AI typically requires a region

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    # Using a text-bison model for summarization
    # For a more production-ready solution, consider fine-tuning or more complex prompt engineering
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("text-bison")

    prompt = f"""Summarize potential quality issues in the following translation. Highlight any discrepancies, awkward phrasing, or potential mistranslations.
Original Text: {original_text}
Translated Text: {translated_text}
Summary of quality issues:"""

    response = model.predict(prompt=prompt, **{
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    })

    return response.text
