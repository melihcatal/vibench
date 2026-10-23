import os
from typing import List, Dict
import boto3
from botocore.exceptions import ClientError


def summarize_transcription(
    transcript_segments: List[Dict[str, str]],
) -> Dict[str, any]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    prompt = "Summarize the following meeting transcript:\n"
    for segment in transcript_segments:
        prompt += f"{segment['text']}\n"

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "temperature": 0.7,
            "topP": 0.9,
        },
    }

    try:
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=bytes(str(body).replace("'", '"'), "utf-8"),
        )
        result = eval(response["body"].read().decode())
        return {
            "summary": result["results"][0]["outputText"].strip(),
            "segments": transcript_segments,
        }
    except ClientError as e:
        raise Exception(f"Failed to summarize transcript: {e}")
