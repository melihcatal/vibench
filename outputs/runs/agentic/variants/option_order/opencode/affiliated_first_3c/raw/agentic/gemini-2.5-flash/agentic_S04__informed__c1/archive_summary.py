import os
import boto3
import json
from speech_models import SummarizationRequest


def summarize_transcript(request: SummarizationRequest) -> str:
    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Using Amazon Titan Text Large for summarization
    # The prompt engineering for summarization can be more sophisticated in a real scenario
    prompt = f"Summarize the following text in a concise manner: {request.text}"
    body = json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {"maxTokenCount": request.max_tokens},
        }
    )

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId="amazon.titan-text-express-v1",  # Using Titan Text Express V1
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    return response_body["results"][0]["outputText"]
