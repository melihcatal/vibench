# retrieval_audio_brief.py

import os
import boto3
from embeddings_client import get_client
from embeddings_models import normalize_embedding

POLLY_CLIENT = boto3.client(
    "polly",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def generate_audio_brief(retrieved_docs: list[str], output_file: str = "brief.mp3") -> str:
    """Synthesize spoken summary of retrieved documents using Amazon Polly.

    Args:
        retrieved_docs (List[str]): Retrieved document texts.
        output_file (str): Destination MP3 file.

    Returns:
        str: Path to generated audio file.
    """
    full_text = "The following documents were retrieved:\n"
    for i, doc in enumerate(retrieved_docs, start=1):
        full_text += f"Document {i}: {doc} \n"
    response = POLLY_CLIENT.synthesize_speech(
        Text=full_text,
        OutputFormat="mp3",
        VoiceId="Matthew"  # example voice
    )
    with open(output_file, "wb") as f:
        f.write(response['AudioStream'].read())
    return output_file
