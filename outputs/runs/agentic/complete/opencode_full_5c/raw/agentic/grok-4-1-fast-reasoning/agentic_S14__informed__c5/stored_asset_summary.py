import boto3
import json
from storage_client import get_s3_client


def stored_asset_summary(bucket_name: str, object_name: str) -> str:
    s3_client = get_s3_client(region="us-east-1")
    obj_response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    text = obj_response["Body"].read().decode("utf-8")[:6000]
    prompt = f"Summarize this asset content concisely:\n\n{text}"
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps(
        {"prompt": prompt, "max_gen_len": 512, "temperature": 0.5, "top_p": 0.9}
    )
    model_id = "meta.llama3-70b-instruct-v1:0"
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["generation"]
