from safety_client import DEFAULT_TRANSLATION_MODEL, get_client, get_model
from safety_models import normalize_text


def appeal_translate(text, target_language="en", model=None):
    client = get_client()
    translation_model = get_model(model, DEFAULT_TRANSLATION_MODEL)
    response = client.responses.create(
        model=translation_model,
        input=[
            {"role": "system", "content": f"Translate the appeal into {target_language}."},
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return {"translation": response.output_text, "raw": response.model_dump()}
