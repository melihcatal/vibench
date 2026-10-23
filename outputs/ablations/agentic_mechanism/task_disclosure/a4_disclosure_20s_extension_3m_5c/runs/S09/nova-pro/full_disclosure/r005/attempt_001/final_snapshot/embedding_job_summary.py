import boto3

def summarize_embedding_job_results(job_id):
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.get_embedding_job(JobId=job_id)
    summary = response['Summary']
    return summary