from speech_client import get_openai_client, get_embedding_model


def transcript_embedding(segments):
    client = get_openai_client()
    texts = [segment.get("text", "") if isinstance(segment, dict) else getattr(segment, "text", "") for segment in segments]
    response = client.embeddings.create(model=get_embedding_model(), input=texts)
    return [item.embedding for item in response.data]
