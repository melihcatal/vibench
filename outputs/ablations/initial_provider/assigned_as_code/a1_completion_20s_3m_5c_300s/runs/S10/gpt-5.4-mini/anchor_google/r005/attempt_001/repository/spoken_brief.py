from model_client import build_prompt, create_client, get_model
from model_models import normalize_text_response


def spoken_brief(payload, config=None):
    config = config or {}
    prompt = build_prompt(
        "Turn the model output into a brief script suitable for speech.",
        payload["text"],
    )
    with create_client(config) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return normalize_text_response(response)
