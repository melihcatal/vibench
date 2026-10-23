import os
from google.cloud import aiplatform
from translation_models import QualitySummaryRequest

def summarize_translation_quality(request: QualitySummaryRequest) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = os.environ.get("VERTEX_AI_GEN_MODEL_ID", "gemini-pro")

    aiplatform.init(project=project_id, location=location)
    
    model = aiplatform.GenerativeModel(model_id)

    prompt = (
        f"You are a translation quality analyst. Analyze the following translation and identify any potential issues "
        f"such as inaccuracies, unnatural phrasing, grammatical errors, or cultural inappropriateness. "
        f"Provide a concise summary of the quality issues found. "
        f"Original ({request.source_language}): \"{request.original_text}\"\n"
        f"Translated ({request.target_language}): \"{request.translated_text}\"\n"
        f"Quality Issues Summary:"
    )
    
    response = model.generate_content(prompt)
    
    return response.candidates[0].content.parts[0].text