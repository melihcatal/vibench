import os, json, boto3

def embed_log_messages(messages, model_id='text-embedding-ada-002'):
    """Embed a list of log messages using Amazon Titan Embeddings via Bedrock Runtime.

    Args:
        messages (list[str]): List of text strings to embed.
        model_id (str): Bedrock model identifier (default Titan Embeddings). 

    Returns:
        list[dict]: Embeddings with original text and vector.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    # Bedrock Runtime client (Titan Embeddings endpoint)
    client = boto3.client('bedrock-runtime', region_name=region)
    embedding_list = []
    for msg in messages:
        # Bedrock expects a list of texts each with a unique id
        response = client.create_embedding(
            ModelId=model_id,
            Text=msg
        )
        # Response contains embedding vector and token count
        embedding = response['embedding']  # 1536-dimensional list of floats
        embedding_list.append({
            'text': msg,
            'embedding': embedding,
            'token_count': response.get('tokens', 0)
        })
    return embedding_list

# Convenience batch wrapper
def batch_embed(log_events):
    texts = []
    for ev in log_events:
        payload = json.loads(ev['message']) if isinstance(ev['message'], str) else ev['message']
        texts.append(payload.get('msg') or payload.get('text') or '')
    return embed_log_messages(texts)
