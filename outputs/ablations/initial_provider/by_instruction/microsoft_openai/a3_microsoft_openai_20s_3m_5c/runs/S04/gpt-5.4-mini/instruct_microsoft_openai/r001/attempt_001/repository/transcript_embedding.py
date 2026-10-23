from speech_client import load_config, openai_post


def transcript_embedding(text: str):
    config = load_config()
    response = openai_post(config, "/embeddings", json={"model": config.openai_embeddings_model, "input": text})
    response.raise_for_status()
    return response.json()
