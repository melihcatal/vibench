import boto3

def summarize_embedding_job(job_id):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.get_embedding_job(jobId=job_id)
    return response