import os
from google.cloud import aiplatform

def stream_completion(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('location') or os.environ.get('GCP_LOCATION', 'us-central1')
    model_id = config.get('model_id') or 'gemini-1.5-flash-001'

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.GenerativeModel(model_id)
    
    prompt = payload.get('prompt', '')
    
    response_stream = model.generate_content(
        contents=prompt,
        stream=True,
        generation_config={
            "max_output_tokens": 1024,
            "temperature": 0.7,
        },
    )
    
    full_response_content = ""
    for chunk in response_stream:
        if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    full_response_content += part.text
    
    return {'streamed_text': full_response_content}
