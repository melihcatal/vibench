import os
from google.cloud import aiplatform

def check_prompt_safety(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = config.get('location') or os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')

    aiplatform.init(project=project_id, location=location)
    
    # For prompt safety, we can leverage the safety attributes returned by the model
    # when making a prediction. Here, we'll simulate a check by making a call
    # and then extracting the safety attributes if available.
    model = aiplatform.Preview.models.ChatModel.from_pretrained("gemini-1.5-flash-001")
    response = model.predict(
        f"""Check the safety of this content: {payload['text']}""",
        temperature=0.0
    )

    safety_attributes = response.safety_attributes.to_dict() if response.safety_attributes else {}
    
    # In a real scenario, you'd analyze safety_attributes to determine safety scores
    # and categories.
    # For this example, we'll just return them directly.
    return {'safety_attributes': safety_attributes}
