import os
from google.cloud import aiplatform

def extract_json(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = config.get('location') or os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.Preview.models.ChatModel.from_pretrained("gemini-1.5-flash-001")
    response = model.predict(
        f"""Extract a JSON object from the following text.
If no JSON is present, return an empty JSON object.

Text:
{payload['text']}

JSON:""",
        temperature=0.0
    )
    return {'json': response.text.strip()}
