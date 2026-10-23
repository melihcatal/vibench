def embedding_job_summary(payload):
    embeddings = payload['embeddings']
    summary = {
        'total_embeddings': len(embeddings),
        'embedding_dimension': len(embeddings[0]) if embeddings else 0,
        'first_embedding_sample': embeddings[0][:5] if embeddings else []  # Show first 5 dimensions as sample
    }
    return summary