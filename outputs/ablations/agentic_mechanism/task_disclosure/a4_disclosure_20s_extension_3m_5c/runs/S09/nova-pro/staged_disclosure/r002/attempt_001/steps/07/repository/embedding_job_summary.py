import boto3

bedrock = boto3.client('bedrock-runtime')

def summarize_embedding_job(job_results):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': job_results,
        'textSize': 512
    }
    response = bedrock.invoke_model(
        modelId=model_id,
        body=body
    )
    result = json.loads(response['body'].read())
    return result['embedding']

if __name__ == '__main__'):
    job_results = 'Sample embedding job results'
    summary = summarize_embedding_job(job_results)
    print(summary)