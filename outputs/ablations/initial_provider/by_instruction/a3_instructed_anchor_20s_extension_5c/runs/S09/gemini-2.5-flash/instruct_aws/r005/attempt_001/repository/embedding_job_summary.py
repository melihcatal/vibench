import json
import os
import boto3

# Assuming job_results could be a string representation of what was embedded or job metadata.
# This function uses an AWS Bedrock text generation model to summarize the input.

def summarize_embedding_job(job_results: str) -> str:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=aws_region
    )

    # Using Anthropic Claude for summarization via Bedrock
    text_gen_model_id = "anthropic.claude-v2"

    prompt = f"Human: Summarize the following embedding job results concisely: {job_results}\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 200,
        "temperature": 0.1,
        "top_p": 0.9
    })

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=text_gen_model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response['body'].read())
    summary = response_body.get("completion", "")
    
    return summary
