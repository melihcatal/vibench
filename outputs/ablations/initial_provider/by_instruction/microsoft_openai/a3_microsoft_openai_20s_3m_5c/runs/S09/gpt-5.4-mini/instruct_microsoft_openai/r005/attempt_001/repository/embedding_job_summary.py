from embeddings_client import get_embedding_client


def embedding_job_summary(job_records):
    client, config = get_embedding_client()
    payload = [record.get("text", "") for record in job_records]
    result = client.embeddings.create(model=config.model, input=payload)
    total = len(job_records)
    embedded = len(result.data)
    return {"model": config.model, "total_records": total, "embedded_records": embedded}
