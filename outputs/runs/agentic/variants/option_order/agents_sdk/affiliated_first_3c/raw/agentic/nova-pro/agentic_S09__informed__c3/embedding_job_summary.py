import boto3

bedrock = boto3.client('bedrock-runtime')

def summarize_embedding_job(job_id):
    response = bedrock.get_embedding_job(jobId=job_id)
    return response