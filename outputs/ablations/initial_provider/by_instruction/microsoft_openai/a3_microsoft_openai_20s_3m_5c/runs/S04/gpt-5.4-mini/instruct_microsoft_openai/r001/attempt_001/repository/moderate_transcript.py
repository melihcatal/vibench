from speech_client import load_config, openai_post


def moderate_transcript(text: str):
    config = load_config()
    response = openai_post(config, "/moderations", json={"model": config.openai_moderation_model, "input": text})
    response.raise_for_status()
    return response.json()
