def summarize_job(results):
    return {'total_embeddings': len(results), 'average_length': sum(len(emb) for emb in results) / len(results) if results else 0}