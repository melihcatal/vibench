from vision_client import get_vision_model
from vision_models import upload_image, parse_vision_response


def score_image_safety(image_path: str) -> dict:
    model = get_vision_model()
    img_file = upload_image(image_path)
    try:
        prompt = 'Evaluate for unsafe content: harassment, hate, sexually explicit, dangerous. {"categories": {"harassment": "NONE|LOW|MED|HIGH", ...}, "overall_risk": "low|medium|high", "recommend_block": false}'
        response = model.generate_content([prompt, img_file])
        return parse_vision_response(response)
    finally:
        img_file.close()
