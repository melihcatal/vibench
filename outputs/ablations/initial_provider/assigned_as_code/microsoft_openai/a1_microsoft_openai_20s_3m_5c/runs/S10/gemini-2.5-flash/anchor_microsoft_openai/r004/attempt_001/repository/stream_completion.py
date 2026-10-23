import os
from google.cloud import aiplatform

def stream_completion(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = config.get('location') or os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.Preview.models.ChatModel.from_pretrained("gemini-1.5-flash-001")
    
    responses = model.predict_streaming(
        f"""{payload['prompt']}"""
    )
    
    # In a real scenario, this would stream tokens back to the client.
    # For this exercise, we'll concatenate them into a single response.
    full_response = ""
    for response in responses:
        full_response += response.text
        
    return {'text': full_response.strip()}
