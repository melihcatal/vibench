from speech_client import load_config, openai_post


def translate_transcript(text: str):
    config = load_config()
    response = openai_post(
        config,
        "/responses",
        json={
            "model": config.openai_translation_model,
            "input": f"Translate this transcript into English:\n{text}",
        },
    )
    response.raise_for_status()
    return response.json()
