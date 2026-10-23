from.embeddings_client import get_text_analytics_client

def embedding_job_summary(job_id):
    client = get_text_analytics_client()
    job_result = client.get_embedding_job(job_id)
    return job_result

if __name__ == '__main__':
    print(embedding_job_summary('sample_job_id'))