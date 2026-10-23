import time
import os
from speech_client import AzureSpeechClient
from speech_models import TranscriptionResponse, TranscriptionResult

def poll_transcription(job_id: str, region: str, api_key: str = None, timeout_seconds: int = 3600):
    client = AzureSpeechClient(region=region, api_key=api_key)
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("Transcription polling timed out.")

        response_json = client.get_transcription(job_id.split('/')[-1]) # Extract job_id from the full URL
        response = TranscriptionResponse(**response_json)

        if response.status == "Succeeded":
            # Fetch files associated with the transcription
            files_json = client.get_transcription_files(job_id.split('/')[-1])
            transcript_file_url = None
            for file_info in files_json.get('values', []):
                if file_info.get('kind') == "Transcription":
                    transcript_file_url = file_info['links']['contentUrl']
                    break
            
            if transcript_file_url:
                transcript_content = client.get_file_content(transcript_file_url)
                return TranscriptionResult(**transcript_content)
            else:
                raise ValueError("Transcription succeeded but no transcript file found.")

        elif response.status in ["Failed", "Cancelled"]:
            raise RuntimeError(f"Transcription job {job_id} {response.status}.")
        
        time.sleep(10) # Poll every 10 seconds
