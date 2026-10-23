import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def archive_summary(text: str, project_id: str, location: str = 'us-central1'):
    # Before running, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file, and gcloud is configured.
    # Example: os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    
    prompt = f"Summarize the following transcript:

{text}

Summary:"

    response = model.generate_content(prompt)
    return response.text
