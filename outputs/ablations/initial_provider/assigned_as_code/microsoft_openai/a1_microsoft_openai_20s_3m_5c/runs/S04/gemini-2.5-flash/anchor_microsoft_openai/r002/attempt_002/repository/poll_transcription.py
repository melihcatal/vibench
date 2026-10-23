import os
import time
import requests
from speech_client import AzureSpeechClient
from speech_models import TranscriptionJobResult, FullTranscriptionResult, normalize_transcription_job_result, parse_full_transcription_result

def poll_transcription(job_id: str, config=None) -> FullTranscriptionResult:
    config = config or {}
    region = config.get('region') or os.environ.get('AZURE_SPEECH_REGION')
    api_key = config.get('api_key') or os.environ.get('AZURE_SPEECH_KEY')

    if not region or not api_key:
        raise ValueError("Azure Speech region and API key must be provided or set as environment variables.")

    client = AzureSpeechClient(region, api_key)

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
                return parse_full_transcription_result(transcript_content_response.json())
            else:
                raise RuntimeError(f"No transcription file found for job {job_id}")
        elif job_result.status == 'Failed':
            raise RuntimeError(f"Transcription job {job_id} failed.")
        elif job_result.status in ['Running', 'NotStarted', 'Waiting', 'Succeeded']:
            # Continue polling
            time.sleep(5)  # Wait for 5 seconds before polling again
        else:
            raise RuntimeError(f"Unknown job status: {job_result.status} for job {job_id}")
