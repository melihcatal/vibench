import boto3


def embedding_job_summary(job_id):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.get_embedding_job(JobId=job_id)
    return response["JobSummary"]
