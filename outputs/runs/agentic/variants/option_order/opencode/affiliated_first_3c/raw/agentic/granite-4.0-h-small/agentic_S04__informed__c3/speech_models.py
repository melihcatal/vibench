# HELPER - Local request/response normalization for AWS Transcribe (Batch Speech-to-Text)
import json
from typing import List, Dict, Any


def normalize_transcript_response(transcript_uri: str) -> List[Dict[str, Any]]:
    """
    Fetch the transcript JSON file from the provided S3 URI and normalize it to a
    simple list of dictionaries containing the word/segment text and start/end times.

    Args:
        transcript_uri (str): S3 URI (e.g., 's3://bucket/key') returned by Transcribe.

    Returns:
        List[Dict]: Normalized list of words/segments with timestamps.
    """
    import boto3

    s3 = boto3.client("s3")
    bucket, key = transcript_uri.replace("s3://", "").split("/", 1)
    obj = s3.get_object(Bucket=bucket, Key=key)
    raw_json = json.loads(obj["Body"].read().decode("utf-8"))
    # Expected structure for Amazon Transcribe (speaker_labels enabled)
    items = []
    for result in raw_json["results"][0]["items"]:
        if result.get("type") == "pronunciation":  # actual word
            items.append(
                {
                    "text": result.get("content", ""),
                    "start_time": result.get("start_time"),
                    "end_time": result.get("end_time"),
                }
            )
    return items


# Example helper to download the file locally (optional)
import tempfile


def download_transcript(transcript_uri: str) -> str:
    bucket, key = transcript_uri.replace("s3://", "").split("/", 1)
    s3 = boto3.client("s3")
    local_path = tempfile.NamedTemporaryFile(delete=False).name
    s3.download_file(bucket, key, local_path)
    return local_path
