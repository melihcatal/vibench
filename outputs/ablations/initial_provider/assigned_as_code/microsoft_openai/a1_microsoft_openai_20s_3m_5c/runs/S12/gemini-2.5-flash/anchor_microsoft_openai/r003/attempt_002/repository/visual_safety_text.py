from vision_client import get_generative_model
from vision_models import normalize_text_safety_response

def visual_safety_text(text: str, config: dict = None) -> dict:
    model = get_generative_model()

    # Use the generative model for content moderation
    prompt = f"""Analyze the following text for any unsafe or inappropriate content. 
Categorize it as safe, potentially unsafe, or unsafe, and provide a brief reason.
Text: """{text}"""
"""

    response = model.generate_content(prompt)
    safety_verdict = response.text

    return normalize_text_safety_response({"verdict": safety_verdict})
