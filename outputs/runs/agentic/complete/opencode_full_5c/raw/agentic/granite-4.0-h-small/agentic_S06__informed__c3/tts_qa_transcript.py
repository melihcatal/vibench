import os
import boto3
from typing import List

# AWS credentials loaded from environment
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

POLICY = {
    "policyType": "TRANSCRIPTION",
    "transcriptionConfig": {
        "languageCode": "en-US",
        "showSpeaker": False,
        "enableAutomaticPunctuation": True,
    },
}

client = boto3.client(
    "transcribe",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def transcribe_audio_file(key: str, dst_bucket: str) -> List[dict]:
    """
    Submit an asynchronous transcription job for a speech file stored in S3.

    Args:
        key (str): S3 object key of the audio file (e.g., "audio.wav").
        dst_bucket (str): Destination S3 bucket to store the transcript JSON.

    Returns:
        List[dict]: The final transcript items as list of dict (utterances).
    """
    job_name = f"tts-qa-{key.replace('.', '_')}-job"
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": f"s3://{os.getenv('S3_BUCKET')}/{key}"},
        OutputBucketName=dst_bucket,
        LanguageCode="en-US",
        ContentRedaction={"RedactionType": "PII"},
    )
    # Poll for completion (simple loop; real-world use would back‑off)
    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in (
            "COMPLETED",
            "FAILED",
        ):
            break
    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "FAILED":
        raise RuntimeError(
            f"Transcription failed: {status['TranscriptionJob']['FailureReason']}"
        )
    transcript = client.get_transcription_job(TranscriptionJobName=job_name)
    result = transcript["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    # Retrieve results from S3 and parse JSON
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    obj = s3.get_object(Bucket=dst_bucket, Key=os.path.basename(result))
    data = obj["Body"].read().decode()
    transcript_json = json.loads(data)
    # Simplify to list of spoken utterances
    utterances = []
    for region in transcript_json.get("results", []):
        for alt in region.get("alternatives", []):
            utterances.append(
                {
                    "start_time": region["start_time"],
                    "end_time": region["end_time"],
                    "text": alt["content"],
                }
            )
    return utterances


# Example (commented)
# items = transcribe_audio_file('sample.wav', 'my-transcripts')
# print(items[:3])
