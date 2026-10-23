import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def embed_metadata_and_text(metadata, extracted_text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-embed-v1'
    try:
        response = bedrock.invoke_model(
            body={
                'inputText': extracted_text,
                'inputMetadata': metadata
            },
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')
        return embedding
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None