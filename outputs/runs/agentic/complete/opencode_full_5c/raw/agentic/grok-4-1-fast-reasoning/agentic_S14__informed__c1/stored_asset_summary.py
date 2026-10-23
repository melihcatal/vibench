from storage_client import s3_config
import boto3
import json


def summarize_stored_asset(bucket: str, key: str) -> str:
    s3_client = boto3.client("s3", **s3_config)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    content = resp["Body"].read().decode("utf-8")
    bedrock_client = boto3.client("bedrock-runtime", **s3_config)
    prompt = f"Human: Provide a concise summary of the following content.\\n\\n{content[:8000]}\\n\\nAssistant:"
    body = json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.7,
                "topP": 0.9,
            },
        }
    )
    model_id = "amazon.titan-text-premier-v1:0"
    resp_model = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    resp_body = json.loads(resp_model["body"].read())
    return resp_body["results"][0]["outputText"].strip()
