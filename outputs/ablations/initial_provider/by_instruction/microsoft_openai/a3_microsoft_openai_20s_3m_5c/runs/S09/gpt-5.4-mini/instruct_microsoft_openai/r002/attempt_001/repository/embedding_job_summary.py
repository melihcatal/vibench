from embeddings_client import get_client, embeddings_model


def embedding_job_summary(job_id: str):
    return get_client().responses.retrieve(job_id, model=embeddings_model())
