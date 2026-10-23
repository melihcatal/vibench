import os
from speech_client import get_transcribe_client
from speech_models import TranscriptionRequest, TranscriptionResult
from poll_transcription import poll_transcription_job, get_transcript_content
import json

def submit_timestamped_transcription_job(request: TranscriptionRequest):
    transcribe_client = get_transcribe_client()
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=request.job_name,
            LanguageCode=request.language_code,
            MediaFormat=request.media_format,
            Media={
                'MediaFileUri': request.media_uri
            },
            OutputBucketName=request.output_bucket,
            Settings={
                'ShowAlternatives': request.show_alternatives
            }
        )
        print(f"Timestamped transcription job {request.job_name} started: {response['TranscriptionJob']['TranscriptionJobStatus']}")
        return response['TranscriptionJob']
    except Exception as e:
        print(f"Error starting timestamped transcription job: {e}")
        raise

def get_timestamped_transcript_result(job_name: str) -> TranscriptionResult:
    job_status = poll_transcription_job(job_name)
    if job_status.status == 'COMPLETED' and job_status.transcript_file_uri:
        transcript_json_content = get_transcript_content(job_status.transcript_file_uri)
        transcript_data = json.loads(transcript_json_content)

        transcript_text = transcript_data['results']['transcripts'][0]['transcript']
        word_timestamps = []

        for item in transcript_data['results']['items']:
            if item['type'] == 'pronunciation':
                word_timestamps.append({
                    'word': item['alternatives'][0]['content'],
                    'start_time': item.get('start_time'),
                    'end_time': item.get('end_time')
                })

        return TranscriptionResult(
            job_name=job_name,
            status=job_status.status,
            transcript_text=transcript_text,
            word_timestamps=word_timestamps,
            segments=None,
            speaker_labels=None
        )
    else:
        return TranscriptionResult(
            job_name=job_name,
            status=job_status.status,
            transcript_text=None,
            word_timestamps=None,
            segments=None,
            speaker_labels=None
        )
