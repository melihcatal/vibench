from vision_client import get_vision_model
from vision_models import upload_image, parse_vision_response


def describe_image(image_path: str) -> dict:
    model = get_vision_model()
    img_file = upload_image(image_path)
    try:
        prompt = 'Provide a short one-sentence visual description of the main content and scene. {"description": "description string"}'
        response = model.generate_content([prompt, img_file])
        return parse_vision_response(response)
    finally:
        img_file.close()
