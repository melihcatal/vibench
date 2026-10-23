import os
import time
import requests
from speech_client import AzureSpeechClient
from speech_models import TranscriptionJobResult, DiarizationSegment, normalize_transcription_job_result, parse_diarized_transcript

def diarized_transcript(audio_uri: str, language_code: str, config=None, job_name: str = "diarized_transcription") -> list[DiarizationSegment]:
    config = config or {}
    region = config.get('region') or os.environ.get('AZURE_SPEECH_REGION')
    api_key = config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY')

    if not region or not api_key:
        raise ValueError("Azure Speech region and API key must be provided or set as environment variables.")

    client = AzureSpeechClient(region, api_key)

    # 1. Submit transcription job with diarization enabled
    submit_response = client.submit_transcription_job(
        display_name=job_name,
        locale=language_code,
        content_urls=[audio_uri],
        diarization_enabled=True
    )
    job_id = submit_response['self'].split('/')[-1]

    # 2. Poll for job completion
    while True:
        job_status_response = client.get_transcription_job(job_id)
        job_result: TranscriptionJobResult = normalize_transcription_job_result(job_status_response)

        if job_result.status == 'Succeeded':
            # Get the files associated with the job
            files_response = client.get_transcription_results(job_id)
            transcript_file_url = None
            for file_info in files_response['values']:
                if file_info['kind'] == 'Transcription':
                    transcript_file_url = file_info['links']['content']
                    break
            
            if transcript_file_url:
                # Fetch the actual transcript content
                transcript_content_response = requests.get(
                    transcript_file_url,
                    headers={'Ocp-Apim-Subscription-Key': api_key},
                    timeout=30
                )
                transcript_content_response.raise_for_status()
                # 3. Parse and return diarized transcript
                return parse_diarized_transcript(transcript_content_response.json())
            else:
                raise RuntimeError(f"No transcription file found for job {job_id}")
        elif job_result.status == 'Failed':
            raise RuntimeError(f"Transcription job {job_id} failed.")
        elif job_result.status in ['Running', 'NotStarted', 'Waiting']:
            # Continue polling
            time.sleep(5)  # Wait for 5 seconds before polling again
        else:
            raise RuntimeError(f"Unknown job status: {job_result.status} for job {job_id}")
