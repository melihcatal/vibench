from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    text = " ".join(payload.get("results", []))
    audio_brief = invoke_bedrock_json(client, model_id, {"inputText": text})
    return {"brief": audio_brief.get("outputText", text[:200])}
