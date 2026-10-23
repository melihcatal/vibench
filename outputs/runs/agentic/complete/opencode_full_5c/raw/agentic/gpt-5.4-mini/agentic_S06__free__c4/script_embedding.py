from speech_client import get_client, embedding_model


def embed_script(text):
    client = get_client()
    result = client.embeddings.create(model=embedding_model(), input=text)
    return result.data[0].embedding
