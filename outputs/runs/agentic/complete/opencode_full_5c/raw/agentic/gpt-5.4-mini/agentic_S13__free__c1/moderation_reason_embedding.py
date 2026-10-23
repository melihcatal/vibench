from safety_client import get_openai_client, embedding_model


def moderation_reason_embedding(text):
    client = get_openai_client()
    res = client.embeddings.create(model=embedding_model(), input=text)
    return {"embedding": res.data[0].embedding}
