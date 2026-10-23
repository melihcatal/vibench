import boto3

def summarize_embedding_job(job_id):
    bedrock = boto3.client('bedrock')
    response = bedrock.summarize_job(JobId=job_id)
    return response

if __name__ == '__main__':\n    job_id = 'example-job-id'\n    summary = summarize_embedding_job(job_id)\n    print(summary)