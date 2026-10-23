import base64
import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def describe_image(payload, config=None):
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    vertexai.init(project=project_id, location=location)

    image_bytes = base64.b64decode(payload["image_bytes"])
    image_part = Part.from_data(data=image_bytes, mime_type="image/jpeg")
    
    model = GenerativeModel("gemini-pro-vision")
    
    response = model.generate_content([image_part, "Describe this image in a short sentence."])

    if not response.candidates:
        raise RuntimeError("No description generated.")
    
    return {"description": response.candidates[0].content.parts[0].text}
