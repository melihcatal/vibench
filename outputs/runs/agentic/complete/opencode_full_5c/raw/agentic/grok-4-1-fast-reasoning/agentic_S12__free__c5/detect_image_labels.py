from vision_client import get_vision_model
from vision_models import upload_image, parse_vision_response


def detect_image_labels(image_path: str) -> dict:
    model = get_vision_model()
    img_file = upload_image(image_path)
    try:
        prompt = 'Identify all objects, scenes, activities, and visual labels in the image. {"labels": ["object1", "label2", ...]}'
        response = model.generate_content([prompt, img_file])
        return parse_vision_response(response)
    finally:
        img_file.close()
