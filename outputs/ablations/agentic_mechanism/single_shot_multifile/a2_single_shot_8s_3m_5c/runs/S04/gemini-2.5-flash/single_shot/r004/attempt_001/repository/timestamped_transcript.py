import speech_client
import speech_models
from typing import List

def get_timestamped_words(job_name: str) -> List[speech_models.WordDetail]:
    transcribe_client = speech_client.get_transcribe_client()
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']
    if job_status != 'COMPLETED':
        raise Exception(f"Transcription job {job_name} is not completed. Current status: {job_status}")
    
    transcript_file_uri = response['TranscriptionJob']['TranscriptFileUri']
    transcribe_json = speech_models.download_and_parse_transcribe_json(transcript_file_uri)
    
    return speech_models.extract_word_details(transcribe_json)