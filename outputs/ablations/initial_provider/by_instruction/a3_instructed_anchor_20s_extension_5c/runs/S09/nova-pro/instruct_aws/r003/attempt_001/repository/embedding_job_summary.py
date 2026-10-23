import boto3

def summarize_embedding_job(job_id):
    client = boto3.client('comprehend')
    response = client.describe_dominant_language_detection_job(JobId=job_id)
    return response['JobStatus']