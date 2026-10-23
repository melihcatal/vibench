import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

bedrock = boto3.client('bedrock-runtime')

def summarize_embedding_job(job_id):
    try:
        response = bedrock.invoke_model(
            model_id='amazon.bedrock.summarization-001',
            body={
                'job_id': job_id,
                'text': 'Embedding job results to be summarized.'
            }
        )
        result = json.loads(response['body'].read())
        return result['summary']
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'Credentials error: {e}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

if __name__ == '__main__':\n    summary = summarize_embedding_job('example-job-id')\n    print(f'Summary: {summary}')
