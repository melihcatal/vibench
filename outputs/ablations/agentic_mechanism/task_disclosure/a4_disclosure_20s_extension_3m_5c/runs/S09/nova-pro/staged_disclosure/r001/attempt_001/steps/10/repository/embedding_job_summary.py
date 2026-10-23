import boto3

def summarize_embedding_job_results(job_id):
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.summarize_embedding_job(JobId=job_id)
    return response['Summary']

if __name__ == '__main__':\n    job_id = 'your-embedding-job-id'
    summary = summarize_embedding_job_results(job_id)
    print(summary)