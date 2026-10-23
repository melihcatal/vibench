import os
import boto3
from google.cloud import genai
from speech_client import get_transcribe_client

def transcript_embedding(aws_bucket, s3_key, model='gemini-pro'):
    # Use Gemini Embeddings API as the concrete provider
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    client = genai.Client()
    # Retrieve transcript from S3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=aws_bucket, Key=s3_key)
    transcript_text = obj['Body'].read().decode('utf-8')
    # Generate embeddings for the whole transcript
    embeddings = client.embed_content(model, parts=[transcript_text])
    vec = embeddings[0]['embedding']  # list of floats
    print(f"Embedding vector length: {len(vec)}")
    # Optional: store vector back to S3 as JSON
    embedding_key = s3_key.replace('.json', '_embedding.json')
    s3.put_object(Bucket=aws_bucket, Key=embedding_key, Body=boto3.s3.transfer.S3Transfer().upload_bytes(bytes(vec)))
    return vec