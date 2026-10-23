from vision_client import call_vision_model
from vision_models import parse_safety_score


def score_image_safety(image_url: str) -> dict:
    prompt = "Evaluate if the image contains unsafe, adult, violent, hateful, or policy-violating visual content. Respond with a risk score from 0 (safe) to 1 (unsafe) and status: safe or unsafe."
    text = call_vision_model(image_url, prompt)
    return parse_safety_score(text)
