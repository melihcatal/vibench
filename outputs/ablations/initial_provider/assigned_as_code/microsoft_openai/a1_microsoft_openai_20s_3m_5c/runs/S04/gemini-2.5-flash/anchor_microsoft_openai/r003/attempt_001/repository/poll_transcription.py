import os
import time
from speech_client import AzureSpeechClient
from speech_models import TranscriptionConfig, TranscriptionJob

def poll_transcription(job: TranscriptionJob, config: TranscriptionConfig, poll_interval_seconds=10):
    client = AzureSpeechClient(config)
    while job.status not in ['SUCCEEDED', 'FAILED']:
        status_response = client.get_transcription_status(job.job_id.split('/')[-1])
        job.status = status_response['status'].upper()
        if job.status == 'SUCCEEDED':
            # Assuming results are available in a 'results' property or similar, 
            # and it contains a 'files' array with 'contentUrl'
            result_url = status_response['links']['files']
            # Now fetch the actual results
            result_files_response = client.get_transcription_result(job.job_id.split('/')[-1], result_url)
            # In Azure Speech-to-Text, the actual transcript is often in a file linked in the 'files' endpoint
            # We need to iterate through the files to find the transcription result
            for file_info in result_files_response['values']:
                if file_info['kind'] == 'Transcription':
                    transcript_content_url = file_info['links']['contentUrl']
                    transcript_result = client.get_transcription_result(job.job_id.split('/')[-1], transcript_content_url)
                    job.results = transcript_result
                    break
        elif job.status == 'FAILED':
            print(f"Transcription job {job.job_id} failed: {status_response.get('properties', {}).get('error')}")
            break
        else:
            time.sleep(poll_interval_seconds)
    return job
