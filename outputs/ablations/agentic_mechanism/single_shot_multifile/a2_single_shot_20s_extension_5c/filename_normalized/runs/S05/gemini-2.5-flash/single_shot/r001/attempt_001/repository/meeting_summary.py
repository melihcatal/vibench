import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel

def summarize_meeting_transcript_chunk(transcript_text, project_id=None, location=None):
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if location is None:
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id or not location:
        raise ValueError("Google Cloud project ID and location must be provided or set in environment variables (GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION).")

    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@002")

    prompt = f"Summarize the following meeting transcript chunk:

{transcript_text}

Summary:"

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }

    response = model.predict(
        prompt,
        **parameters
    )
    return response.text