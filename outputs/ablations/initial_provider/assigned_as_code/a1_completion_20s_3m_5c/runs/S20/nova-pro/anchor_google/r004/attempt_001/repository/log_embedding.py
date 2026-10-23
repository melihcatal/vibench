import boto3

def embed_log_message(log_message):
    sagemaker = boto3.client('sagemaker-runtime')
    response = sagemaker.invoke_endpoint(
        EndpointName='my-sagemaker-endpoint',
        ContentType='text/plain',
        Body=log_message
    )
    return response['Body'].read()

if __name__ == '__main__':
    log_message = 'This is a sample log message.'
    embedding = embed_log_message(log_message)
    print(embedding)