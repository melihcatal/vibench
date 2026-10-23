import embeddings_client

def embed_batch(payloads, config=None):
    client = embeddings_client.get_client(config)
    embeddings = []
    for payload in payloads:
        normalized_payload = embeddings_client.normalize_payload(payload)
        response = client.embeddings.create(model='text-embedding-3-small', input=normalized_payload['text'])
        embeddings.append(embeddings_client.parse_response(response))
    return embeddings