import boto3

from speech_models import TranscriptChunk


def caption_embedding(chunks):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    for chunk in chunks:
        client.invoke_model(modelId="amazon.titan-embed-text-v1", body=chunk.text.encode())
        yield TranscriptChunk(text=chunk.text, is_final=chunk.is_final)
