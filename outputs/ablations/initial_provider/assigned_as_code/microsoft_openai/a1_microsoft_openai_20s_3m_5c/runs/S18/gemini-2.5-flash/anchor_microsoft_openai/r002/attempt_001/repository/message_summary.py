import os
import vertexai
from vertexai.language_models import TextGenerationModel

def summarize_message_content(text_content):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")
    
    prompt = f"Summarize the following text:

{text_content}"

    response = model.predict(prompt=prompt)
    return {"summary": response.text}
