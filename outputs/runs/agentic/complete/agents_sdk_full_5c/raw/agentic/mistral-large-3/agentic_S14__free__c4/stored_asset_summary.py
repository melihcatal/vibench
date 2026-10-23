import boto3
from storage_client import get_storage_client

def summarize_stored_asset(bucket_name: str, object_key: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> dict:
    s3_client = get_storage_client()
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        text = response['Body'].read().decode('utf-8')

        prompt = f"Summarize the following content in 3-5 bullet points:\n\n{text}"
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 400,
            "messages": [{"role": "user", "content": prompt}]
        }

        bedrock_response = bedrock_client.invoke_model(
            modelId=model_id,
            body=bytes(str(body), 'utf-8')
        )
        result = bedrock_response['body'].read().decode('utf-8')
        summary = eval(result)['content'][0]['text']

        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "summary": summary,
            "success": True
        }
    except Exception as e:
        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "success": False,
            "error": str(e)
        }