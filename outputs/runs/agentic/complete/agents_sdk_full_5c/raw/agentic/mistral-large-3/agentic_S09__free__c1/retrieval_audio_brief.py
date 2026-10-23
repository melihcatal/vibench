import os
from typing import List, Dict
from gtts import gTTS
import boto3
from botocore.exceptions import ClientError

def generate_audio_brief(search_results: List[Dict], output_file: str) -> str:
    brief_text = "Top results: " + ". ".join([
        f"Result {i+1}: {result['text']}" for i, result in enumerate(search_results[:3])
    ])
    
    tts = gTTS(text=brief_text, lang='en')
    tts.save(output_file)
    
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(
            output_file,
            "audio-briefs-bucket",
            f"briefs/{os.path.basename(output_file)}"
        )
        return f"s3://audio-briefs-bucket/briefs/{os.path.basename(output_file)}"
    except ClientError as e:
        raise Exception(f"Failed to upload audio brief to S3: {e}")