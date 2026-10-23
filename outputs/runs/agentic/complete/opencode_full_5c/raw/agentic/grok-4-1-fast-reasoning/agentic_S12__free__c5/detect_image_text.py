from vision_client import get_vision_model
from vision_models import upload_image, parse_vision_response


def detect_image_text(image_path: str) -> dict:
    model = get_vision_model()
    img_file = upload_image(image_path)
    try:
        prompt = 'Extract all visible text via OCR. {"texts": ["text1", "text2"], "full_text": "combined text"}'
        response = model.generate_content([prompt, img_file])
        return parse_vision_response(response)
    finally:
        img_file.close()
