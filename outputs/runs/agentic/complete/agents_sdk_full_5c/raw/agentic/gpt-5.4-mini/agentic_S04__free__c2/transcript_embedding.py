from speech_client import get_client


def transcript_embedding(text: str):
    client = get_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
    )
    vector = response.data[0].embedding
    return {"vector": vector, "raw": response.model_dump()}
