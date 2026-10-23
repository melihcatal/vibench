from embeddings_client import get_client, get_config, invoke_embedding


def retrieval_audio_brief(payload, config=None):
    config = get_config(config)
    client = get_client(config)
    raw = invoke_embedding(client, config["model_id"], {"inputText": payload["brief_text"]})
    return {"audio_brief": raw}
