import embeddings_client

def summarize_embedding_job(job_results):
    client = embeddings_client.get_client()
    summary = {'total_embeddings': len(job_results), 'average_length': sum(len(embedding['embedding']) for embedding in job_results) / len(job_results)}
    return summary