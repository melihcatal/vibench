from model_client import client_from_config, get_model_name


def spoken_brief(payload, config=None):
    config = config or {}
    prompt = "Rewrite the following as a brief spoken script.\n\n" + payload["text"]
    with client_from_config(config) as client:
        response = client.models.generate_content(model=get_model_name(config), contents=prompt)
    return {"text": response.text or ""}
