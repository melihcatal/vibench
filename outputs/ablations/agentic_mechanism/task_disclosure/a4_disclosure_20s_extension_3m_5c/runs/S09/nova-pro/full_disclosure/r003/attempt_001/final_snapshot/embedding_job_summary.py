import boto3

bedrock = boto3.client('bedrock-runtime')

def summarize_embedding_job_results(job_id):
    response = bedrock.get_embedding_job(JobId=job_id)
    summary = {
        'job_id': response['JobId'],
        'status': response['Status'],
        'created_at': response['CreatedAt'],
        'completed_at': response['CompletedAt'],
        'input_count': response['InputCount'],
        'output_count': response['OutputCount'],
    }
    return summary