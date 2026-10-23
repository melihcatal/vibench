from model_client import client_from_config, get_model_name


def result_translate(payload, config=None):
    config = config or {}
    source_text = payload["text"]
    target_language = payload.get("language", "English")
    prompt = "Translate the following text into " + target_language + ".\n\n" + source_text
    with client_from_config(config) as client:
        response = client.models.generate_content(model=get_model_name(config), contents=prompt)
    return {"text": response.text or ""}
