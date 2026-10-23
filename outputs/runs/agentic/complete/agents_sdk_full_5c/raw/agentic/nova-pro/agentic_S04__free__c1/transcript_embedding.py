from speech_client import get_sagemaker_runtime_client

def transcript_embedding(text):
    sagemaker_runtime = get_sagemaker_runtime_client()
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName='text-embedding-endpoint',
        ContentType='text/plain',
        Body=text
    )
    return response