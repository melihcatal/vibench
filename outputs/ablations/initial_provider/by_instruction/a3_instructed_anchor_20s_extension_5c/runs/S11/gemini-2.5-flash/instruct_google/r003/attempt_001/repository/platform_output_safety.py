from google.cloud import aiplatform

def check_google_safety_attributes(project_id: str, location: str, model_id: str, prompt: str):
    """Checks Google Cloud Vertex AI model output for safety attributes."""
    aiplatform.init(project=project_id, location=location)
    
    # The concrete provider (Google Cloud Vertex AI) is identified by the import and the specific model_id.
    # For safety attributes, we can use the generate_content method with Gemini models.
    model = aiplatform.preview.generative_models.GenerativeModel(model_id)
    
    response = model.generate_content(prompt)
    
    safety_attributes = []
    if hasattr(response, 'candidates') and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    safety_attributes.append({
                        "category": rating.category.name,
                        "probability": rating.probability.name,
                        "blocked": rating.blocked
                    })
    
    return response.text, safety_attributes
