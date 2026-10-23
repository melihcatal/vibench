import time
from speech_client import AzureSpeechClient
from speech_models import TranscriptionResult

def poll_transcription(job_id: str, client: AzureSpeechClient, timeout_seconds: int = 600) -> TranscriptionResult:
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        job_details = client.get_transcription_job(job_id)
        status = job_details['status']

        if status == 'Succeeded':
            # Azure Speech-to-Text provides a 'files' URL for the results
            files_url = job_details['links']['files']
            files_response = client.get_transcription_result(files_url)
            
            # Find the file that contains the actual transcript (typically a JSON file)
            transcript_file_url = None
            for file_item in files_response['values']:
                if file_item['kind'] == 'Transcription' and file_item['properties']['dataType'] == 'Result':
                    transcript_file_url = file_item['links']['contentUrl']
                    break
            
            if transcript_file_url:
                transcript_content = client.get_transcription_result(transcript_file_url)
                full_transcript = " ".join([phrase['display'] for segment in transcript_content['recognizedPhrases'] for phrase in [segment]])
                return TranscriptionResult(job_id=job_id, status=status, transcript=full_transcript)
            else:
                return TranscriptionResult(job_id=job_id, status=status, transcript=None) # Should not happen for successful jobs
        elif status in ['Failed', 'Cancelled']:
            return TranscriptionResult(job_id=job_id, status=status)
        
        time.sleep(5)  # Wait for 5 seconds before polling again
    
    return TranscriptionResult(job_id=job_id, status="Timeout", transcript=None)
