import bedrock

def summarize_embedding_job_results(job_id):
    client = bedrock.client()
    response = client.get_embedding_job(job_id=job_id)
    summary = {
        'job_id': response['job_id'],
        'status': response['status'],
        'total_documents': response['total_documents'],
        'successful_documents': response['successful_documents'],
        'failed_documents': response['failed_documents'],
        'duration': response['duration']
    }
    return summary