import boto3

from speech_models import TranscriptChunk


def meeting_summary(chunks):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    prompt = "\n".join(chunk.text for chunk in chunks)
    client.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0", body=prompt.encode())
    return TranscriptChunk(text=prompt[:200], is_final=True)
