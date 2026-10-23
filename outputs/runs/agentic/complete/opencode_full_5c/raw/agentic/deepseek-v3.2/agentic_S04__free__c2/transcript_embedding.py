import boto3
import numpy as np
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from speech_models import TranscriptionResult


def transcript_embedding(
    transcript_result: TranscriptionResult, segment_size: int = 100
) -> dict:
    """
    Embed transcript segments for semantic retrieval using AWS Bedrock Titan Embeddings.

    Args:
        transcript_result: TranscriptionResult object
        segment_size: Number of words per segment for embedding

    Returns:
        Dictionary containing embeddings and metadata
    """
    # Create AWS Bedrock client
    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    # Create S3 client for storing embeddings
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        # Split transcript into segments
        words = transcript_result.transcript.split()
        segments = []

        for i in range(0, len(words), segment_size):
            segment_text = " ".join(words[i : i + segment_size])
            segments.append(
                {
                    "segment_id": f"segment_{i // segment_size}",
                    "text": segment_text,
                    "word_start": i,
                    "word_end": min(i + segment_size, len(words)),
                }
            )

        # Generate embeddings for each segment using AWS Bedrock Titan Embeddings
        embeddings = []

        for segment in segments:
            # Prepare request for Titan Embeddings model
            request_body = json.dumps({"inputText": segment["text"]})

            # Call Bedrock Titan Embeddings model
            response = bedrock_client.invoke_model(
                modelId="amazon.titan-embed-text-v1",
                contentType="application/json",
                accept="application/json",
                body=request_body,
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            embeddings.append(
                {
                    "segment_id": segment["segment_id"],
                    "embedding": embedding,
                    "text": segment["text"],
                    "embedding_dimensions": len(embedding),
                }
            )

        # Calculate average embedding for the entire transcript
        if embeddings:
            all_embeddings = np.array([e["embedding"] for e in embeddings])
            average_embedding = np.mean(all_embeddings, axis=0).tolist()
        else:
            average_embedding = []

        # Store embeddings in S3
        bucket_name = os.environ.get(
            "AWS_EMBEDDINGS_BUCKET", "transcript-embeddings-bucket"
        )
        embeddings_key = f"embeddings/{transcript_result.job_id}/embeddings.json"

        embeddings_data = {
            "job_id": transcript_result.job_id,
            "segments": embeddings,
            "average_embedding": average_embedding,
            "segment_count": len(segments),
            "embedding_model": "amazon.titan-embed-text-v1",
            "created_at": datetime.now().isoformat(),
        }

        s3_client.put_object(
            Bucket=bucket_name,
            Key=embeddings_key,
            Body=json.dumps(embeddings_data, indent=2),
            ContentType="application/json",
        )

        # Create search index metadata
        search_index = {
            "job_id": transcript_result.job_id,
            "embeddings_location": f"s3://{bucket_name}/{embeddings_key}",
            "segment_embeddings": [
                {
                    "segment_id": e["segment_id"],
                    "text_preview": e["text"][:100] + "..."
                    if len(e["text"]) > 100
                    else e["text"],
                    "embedding_dimensions": e["embedding_dimensions"],
                }
                for e in embeddings
            ],
            "average_embedding_dimensions": len(average_embedding)
            if average_embedding
            else 0,
        }

        return {
            "job_id": transcript_result.job_id,
            "segment_count": len(segments),
            "embeddings_generated": len(embeddings),
            "embedding_model": "amazon.titan-embed-text-v1",
            "embeddings_stored_at": f"s3://{bucket_name}/{embeddings_key}",
            "search_index": search_index,
            "embedding_service": "aws_bedrock",
        }

    except ClientError as e:
        print(f"Error generating embeddings: {e}")
        raise


import os
import json
from datetime import datetime
