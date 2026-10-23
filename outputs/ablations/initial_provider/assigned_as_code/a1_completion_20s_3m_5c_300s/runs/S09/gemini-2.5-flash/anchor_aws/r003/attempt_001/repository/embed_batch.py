from embeddings_client import BedrockEmbeddingsClient

def embed_batch(payload, config=None):
    config = config or {}
    client = BedrockEmbeddingsClient(
        region_name=config.get("region"),
        model_id="amazon.titan-embed-text-v2:0"
    )
    texts = payload["texts"]
    # The client-side batching for Bedrock model, as Bedrock invoke_model is not inherently batch-enabled for this model.
    embeddings_data = client.invoke_model_batch(texts)
    return embeddings_data
