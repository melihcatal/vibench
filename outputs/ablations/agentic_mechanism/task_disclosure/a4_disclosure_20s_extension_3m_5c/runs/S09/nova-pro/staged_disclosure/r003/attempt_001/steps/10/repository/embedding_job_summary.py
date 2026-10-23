import boto3

def summarize_embedding_job_results(job_id):
    bedrock = boto3.client('bedrock')
    response = bedrock.get_embedding_job(jobId=job_id)
    summary = response['summary']
    return summary

if __name__ == '__main__':
    job_id = 'your-embedding-job-id'
    summary = summarize_embedding_job_results(job_id)
    print(summary)