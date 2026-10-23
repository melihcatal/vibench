import os
import google.cloud.aiplatform as aiplatform

def check_text_safety(text: str, project_id: str = None, location: str = 'us-central1') -> dict:
    if project_id is None:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name="gemini-pro")

    response = model.generate_content([text])

    safety_attributes = {
        'harms_detected': False,
        'safety_ratings': []
    }

    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes['safety_ratings'].append({
                'category': rating.category.name,
                'probability': rating.probability.name,
                'blocked': rating.blocked
            })
            if rating.blocked:
                safety_attributes['harms_detected'] = True

    return safety_attributes