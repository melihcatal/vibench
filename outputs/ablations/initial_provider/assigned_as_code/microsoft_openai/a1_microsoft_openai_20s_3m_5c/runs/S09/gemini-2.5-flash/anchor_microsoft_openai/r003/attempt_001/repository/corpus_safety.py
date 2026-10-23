import os
from google.cloud import aiplatform

def corpus_safety(payload: dict, config: dict = None) -> dict:
    config = config or {}
    project = config.get("google_cloud_project") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("google_cloud_location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        raise ValueError("Google Cloud project not provided or found in environment variables.")

    aiplatform.init(project=project, location=location)

    # Using a specific model for content moderation (e.g., gemini-pro with safety settings)
    model_name = config.get("safety_model") or "gemini-pro" 
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)

    texts_to_check = payload.get("texts", [])
    safety_results = []

    for text in texts_to_check:
        response = model.predict(text)
        is_safe = True
        safety_attributes_summary = {}

        if hasattr(response, 'safety_attributes') and response.safety_attributes:
            categories = response.safety_attributes.categories
            scores = response.safety_attributes.scores
            
            for i, category in enumerate(categories):
                safety_attributes_summary[category] = scores[i]
                # If any score for a harmful category is above a threshold, consider it unsafe
                # This threshold might need tuning based on actual use case
                if scores[i] > 0.7:  # Example threshold
                    is_safe = False
                    
        safety_results.append({
            "text": text,
            "is_safe": is_safe,
            "safety_attributes": safety_attributes_summary
        })

    return {"safety_checks": safety_results}
