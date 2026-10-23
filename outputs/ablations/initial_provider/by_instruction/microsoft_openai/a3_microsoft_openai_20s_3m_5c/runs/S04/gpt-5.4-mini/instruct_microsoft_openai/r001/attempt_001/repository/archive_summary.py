from speech_client import load_config, openai_post


def archive_summary(text: str):
    config = load_config()
    response = openai_post(
        config,
        "/responses",
        json={
            "model": config.openai_translation_model,
            "input": f"Summarize this transcription result for archival storage:\n{text}",
        },
    )
    response.raise_for_status()
    return response.json()
