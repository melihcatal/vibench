import os
import base64
from google.cloud import aiplatform
from vision_models import ImageInput, ImageDescriptionResult

def describe_image(image_input: ImageInput) -> ImageDescriptionResult:
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    model_name = 'gemini-pro-vision'
    model = aiplatform.GenerativeModel(model_name)

    contents = []
    if image_input.content_base64:
        image_bytes = base64.b64decode(image_input.content_base64)
        contents.append(aiplatform.types.Blob(mime_type='image/jpeg', data=image_bytes))
    elif image_input.image_uri and image_input.image_uri.startswith('gs://'):
        contents.append(aiplatform.types.FileData(mime_type='image/jpeg', file_uri=image_input.image_uri))
    else:
        raise ValueError("ImageInput must contain content_base64 or a GCS image_uri (gs://...). Other URIs are not directly supported by Gemini Pro Vision without explicit download.")

    contents.append('Describe this image concisely.')

    response = model.generate_content(contents)

    description = response.candidates[0].content.parts[0].text.strip()
    return ImageDescriptionResult(description=description)