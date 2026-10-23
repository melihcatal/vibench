import boto3
import json

def asset_metadata_embedding(bucket: str, key: str) -> list[float]:
    """
    Embeds object metadata and extracted text using Amazon Titan Embeddings via Bedrock.
    Assumes UTF-8 text file.
    """
    s3_client = boto3.client('s3')
    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    metadata_str = json.dumps(head_response.get('Metadata', {}))
    
    get_response = s3_client.get_object(Bucket=bucket, Key=key)
    text = get_response['Body'].read().decode('utf-8')[:8000]
    
    input_text = f"Metadata: {metadata_str}\nText: {text}"
    
    bedrock_client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v2:0'
    
    body = json.dumps({
        "inputText": input_text
    })
    
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        contentType='application/json',
        accept='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['embedding']