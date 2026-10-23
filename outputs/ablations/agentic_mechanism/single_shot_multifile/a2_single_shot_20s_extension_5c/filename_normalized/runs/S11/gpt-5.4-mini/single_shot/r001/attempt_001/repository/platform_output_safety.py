from google import genai
from model_client import get_platform_client, get_platform_model_id
from model_models import normalize_platform_text


def platform_output_safety(text, safety_prompt=None):
    client = get_platform_client()
    model_id = get_platform_model_id()
    prompt = safety_prompt or "Assess whether the following content is unsafe, harmful, or disallowed. Return a concise yes or no with brief reason. Content:"
    response = client.models.generate_content(
        model=model_id,
        contents=f"{prompt} {normalize_platform_text(text)}",
    )
    return response.text if hasattr(response, "text") else str(response)
