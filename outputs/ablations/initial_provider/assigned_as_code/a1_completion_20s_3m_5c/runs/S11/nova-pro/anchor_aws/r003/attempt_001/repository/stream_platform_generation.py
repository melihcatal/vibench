import boto3

def stream_platform_generation(model_id, prompt):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        modelId=model_id,
        body={
            'prompt': prompt,
            'max_tokens': 150
        }
    )
    return response