from typing import List, Dict
import os
import boto3

def generate_audio_brief(results: List[Dict], output_s3_path: str) -> str:
    polly_client = boto3.client('polly')
    
    brief_text = "Here are the top results: " + ". ".join(
        [f"Result {i+1}: {result['text']}" for i, result in enumerate(results[:3])]
    )
    
    response = polly_client.synthesize_speech(
        Text=brief_text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )
    
    s3_client = boto3.client('s3')
    bucket, key = output_s3_path.replace("s3://", "").split("/", 1)
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=response['AudioStream'].read()
    )
    
    return output_s3_path