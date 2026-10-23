import time
import os
from speech_client import AzureSpeechClient
from speech_models import TranscriptionConfig, TranscriptionJob, TranscriptionResult

def poll_transcription(job: TranscriptionJob, config: TranscriptionConfig = None, poll_interval_seconds: int = 5):
    config = config or TranscriptionConfig()
    client = AzureSpeechClient(config)

    job_id = job.job_id.split('/')[-1] # Extract actual job ID from the self URI

    while True:
        job_status_response = client.get_transcription_job(job_id)
        status = job_status_response['status']
        if status == 'Succeeded':
            files_uri = job_status_response['links']['files']
            files_response = requests.get(files_uri, headers=client._get_headers())
            files_response.raise_for_status()
            files_data = files_response.json()

            for file_item in files_data['values']:
                if file_item['kind'] == 'Transcription' and file_item['properties']['contentType'] == 'application/json':
                    transcript_result = client.get_transcription_result(file_item['links']['contentUrl'])
                    return TranscriptionResult.parse_obj(transcript_result)
            raise Exception("Transcription result not found in job files.")
        elif status == 'Failed':
            raise Exception(f"Transcription job failed: {job_status_response.get('properties', {}).get('error', 'Unknown error')}")
        else:
            print(f"Transcription job status: {status}. Polling again in {poll_interval_seconds} seconds...")
            time.sleep(poll_interval_seconds)

