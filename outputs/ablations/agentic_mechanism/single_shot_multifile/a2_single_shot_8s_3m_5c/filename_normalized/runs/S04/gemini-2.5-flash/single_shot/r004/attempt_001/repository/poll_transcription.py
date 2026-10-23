import time
import speech_client
import speech_models

def poll_and_get_transcript(job_name: str, wait_interval_seconds: int = 10) -> str:
    transcribe_client = speech_client.get_transcribe_client()
    
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status == 'COMPLETED':
            transcript_file_uri = response['TranscriptionJob']['TranscriptFileUri']
            transcribe_json = speech_models.download_and_parse_transcribe_json(transcript_file_uri)
            return speech_models.extract_full_transcript_text(transcribe_json)
        elif job_status == 'FAILED':
            raise Exception(f"Transcription job {job_name} failed: {response['TranscriptionJob'].get('FailureReason')}")
        else:
            time.sleep(wait_interval_seconds)