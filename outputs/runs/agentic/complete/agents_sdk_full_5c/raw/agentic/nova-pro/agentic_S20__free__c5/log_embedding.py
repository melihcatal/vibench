from observability_client import SAGEMAKER

def embed_text(text):
    response = SAGEMAKER.invoke_endpoint(
        EndpointName='my-embedding-endpoint',
        ContentType='text/plain',
        Body=text
    )
    return response['Body'].read()

text = 'This is a sample log message.'
embedding = embed_text(text)
print(embedding)