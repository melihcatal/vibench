import time
import requests
from speech_client import AzureSpeechClient
from speech_models import TranscriptionResult

def poll_transcription(job_id: str, client: AzureSpeechClient, timeout_seconds: int = 600, poll_interval_seconds: int = 10):
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        try:
            job_details = client.get_transcription(job_id)
            result = TranscriptionResult(id=job_details['self'],
                                         status=job_details['status'],
                                         locale=job_details['locale'],
                                         createdDateTime=job_details['createdDateTime'],
                                         lastActionDateTime=job_details['lastActionDateTime'],
                                         displayName=job_details['displayName'],
                                         links=job_details['links'],
                                         properties=job_details['properties'])
            
            if result.status == "Succeeded":
                # Find the 'result' file link
                files_response = client.get_transcription_files(job_id)
                transcript_file_url = None
                for file_item in files_response['values']:
                    if file_item['kind'] == 'Transcription':
                        transcript_file_url = file_item['links']['contentUrl']
                        break
                
                if transcript_file_url:
                    transcript_content_response = requests.get(transcript_file_url)
                    transcript_content_response.raise_for_status()
                    return transcript_content_response.json()
                else:
                    raise RuntimeError("Transcription succeeded but no result file found.")
            elif result.status in ["Failed", "Cancelled"]:
                raise RuntimeError(f"Transcription job {job_id} {result.status}.")
        except requests.exceptions.RequestException as e:
            print(f"Error polling transcription job: {e}")
        
        time.sleep(poll_interval_seconds)
    
    raise TimeoutError(f"Transcription job {job_id} did not complete within {timeout_seconds} seconds.")
