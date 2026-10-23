import boto3

def summarize_embedding_job_results(job_id):
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.get_embedding_job(JobId=job_id)
    if response['Status'] == 'COMPLETED':
        summary = f'Embedding job {job_id} completed successfully.'
    else:
        summary = f'Embedding job {job_id} is still running or failed.'
    return summary