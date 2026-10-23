from typing import Iterable

import boto3


def summarize_meeting_transcript(chunks: Iterable[str], model_id: str = "anthropic.claude-3-haiku-20240307-v1:0") -> str:
    client = boto3.client("bedrock-runtime")
    transcript = "\n".join(chunk for chunk in chunks if chunk)
    body = f'{{"anthropic_version":"bedrock-2023-05-31","max_tokens":300,"messages":[{{"role":"user","content":[{{"type":"text","text":"Summarize this meeting transcript:\n{transcript}"}}]}}]}}'
    response = client.invoke_model(modelId=model_id, body=body, contentType="application/json", accept="application/json")
    return response["body"].read().decode("utf-8")
