import boto3

from speech_client import get_transcribe_client


def archive_summary(job_id, config=None):
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    if job["TranscriptionJobStatus"]!= "COMPLETED":
        raise ValueError("Transcription job is not completed")
    transcript_uri = job["Transcript"]["TranscriptFileUri"]
    s3 = boto3.client('s3', region_name=config.get('region'))
    bucket_name = config.get('bucket_name')
    object_key = f"transcriptions/{job_id}/summary.txt"
    s3.upload_file(transcript_uri, bucket_name, object_key)
    return f"s3://{bucket_name}/{object_key}"
