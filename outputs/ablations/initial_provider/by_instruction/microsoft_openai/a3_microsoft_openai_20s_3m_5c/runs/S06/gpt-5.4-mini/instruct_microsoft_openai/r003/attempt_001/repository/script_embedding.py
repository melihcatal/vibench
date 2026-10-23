from speech_client import client, embedding_model


def embed_script(script: str):
    response = client().embeddings.create(model=embedding_model(), input=script)
    return response.data[0].embedding
