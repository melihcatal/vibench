from model_client import build_prompt, create_client, get_model
from model_models import normalize_text_response


def result_translate(payload, config=None):
    config = config or {}
    prompt = build_prompt(
        "Translate the following model output into the target language.",
        f"Target language: {payload['target_language']}",
        payload["text"],
    )
    with create_client(config) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return normalize_text_response(response)
