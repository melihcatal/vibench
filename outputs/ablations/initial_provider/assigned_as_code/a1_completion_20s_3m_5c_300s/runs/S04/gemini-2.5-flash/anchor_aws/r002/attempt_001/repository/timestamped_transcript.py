import json
import requests

from speech_client import SpeechClient
from speech_models import TimestampedTranscriptRequest, parse_transcription_result


def timestamped_transcript(request: TimestampedTranscriptRequest, config=None) -> dict:
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_transcribe_client()

    response = client.get_transcription_job(TranscriptionJobName=request.job_id)
    job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    if job_status == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

        # In a real application, you would fetch the content from the S3 URI.
        # For this exercise, we'll use the helper to simulate parsing.
        # This assumes the transcription job was configured to output word-level timestamps.
        # Example of how you might fetch content:
        # s3_object_url = transcript_uri
        # transcript_content_response = requests.get(s3_object_url)
        # transcript_data = json.loads(transcript_content_response.text)
        
        transcript_data = parse_transcription_result(transcript_uri) # Mock parsing

        word_timestamps = []
        for result in transcript_data["results"]:
            for alternative in result["alternatives"]:
                if "words" in alternative:
                    word_timestamps.extend(alternative["words"])
        
        return {"job_id": request.job_id, "word_timestamps": word_timestamps}

    elif job_status == "FAILED":
        raise Exception(f"Transcription job {request.job_id} failed: {response['TranscriptionJob'].get('FailureReason')}")
    else:
        raise Exception(f"Transcription job {request.job_id} is not yet completed. Current status: {job_status}")
