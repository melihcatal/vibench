from speech_client import AzureSpeechClient
from speech_models import TranscriptionConfig, TranscriptionResult
from poll_transcription import poll_transcription
import typing

def diarized_transcript(audio_uri: str, language_code: str, client: AzureSpeechClient) -> TranscriptionResult:
    config = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        diarization_enabled=True,
        display_name="diarized_transcription_job"
    )
    
    submit_response = client.submit_transcription_job(config)
    job_id = submit_response['self'].split('/')[-1] # Extract job_id from the 'self' URL

    # Poll for the transcription result
    transcription_result = poll_transcription(job_id, client)

    if transcription_result.status == "Succeeded" and transcription_result.transcript is not None:
        # Fetch detailed results for diarization
        job_details = client.get_transcription_job(job_id)
        files_url = job_details['links']['files']
        files_response = client.get_transcription_result(files_url)

        transcript_file_url = None
        for file_item in files_response['values']:
            if file_item['kind'] == 'Transcription' and file_item['properties']['dataType'] == 'Result':
                transcript_file_url = file_item['links']['contentUrl']
                break
        
        if transcript_file_url:
            transcript_content = client.get_transcription_result(transcript_file_url)
            speaker_segments = []
            for segment in transcript_content['recognizedPhrases']:
                speaker_segments.append({
                    'speaker': segment['speaker'],
                    'text': segment['display'],
                    'offset': segment['offsetInTicks'],
                    'duration': segment['durationInTicks']
                })
            transcription_result.speaker_segments = speaker_segments

    return transcription_result
