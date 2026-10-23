from speech_client import get_client, get_embedding_model


def transcript_embedding(segments):
    client = get_client()
    text = "\n".join(segment.get("text", "") for segment in segments)
    response = client.embeddings.create(model=get_embedding_model(), input=text)
    return response.data[0].embedding
