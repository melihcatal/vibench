import os
from google.cloud import aiplatform

def check_prompt_safety(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('location') or os.environ.get('GCP_LOCATION', 'us-central1')
    model_id = config.get('model_id') or 'gemini-1.5-flash-001'

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.GenerativeModel(model_id)
    
    prompt = payload.get('prompt', '')
    
    # Vertex AI GenerativeModel automatically includes safety attributes in the response
    response = model.generate_content(contents=prompt)
    
    safety_attributes = None
    if response.candidates and response.candidates[0].safety_ratings:
        safety_attributes = [
            {"category": rating.category.name, "probability": rating.probability.name}
            for rating in response.candidates[0].safety_ratings
        ]
            
    return {
        'prompt': prompt,
        'safety_attributes': safety_attributes,
        'generated_content': response.candidates[0].content.parts[0].text if response.candidates and response.candidates[0].content and response.candidates[0].content.parts else ""
    }
