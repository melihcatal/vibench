import boto3

bedrock = boto3.client('bedrock-runtime')

def summarize_embedding_job(job_results):
    model_id = 'amazon.titan-embed-text-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': job_results
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    summary = response_body.get('embedding')

    return summary

if __name__ == '__main__':
    job_results = 'Sample embedding job results'
    summary = summarize_embedding_job(job_results)
    print(f'Summary: {summary}')
