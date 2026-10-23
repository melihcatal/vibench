import boto3

from speech_client import get_transcribe_client


def diarized_transcript(job_id, config=None):
    config = config or {}
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    if job["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = job["Transcript"]["TranscriptFileUri"]
        response = client.get_object(Bucket=config["bucket"], Key=transcript_uri.split("/")[-1])
        transcript_content = response["Body"].read().decode('utf-8')
        import json
        transcript_data = json.loads(transcript_content)
        diarized_segments = transcript_data.get("results", {}).get("speaker_labels", {}).get("segments", [])
        return diarized_segments
    return []