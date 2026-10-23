from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    translated = invoke_bedrock_json(client, model_id, {"inputText": payload["query"]})
    return {"translated_query": translated.get("outputText", payload["query"])}
