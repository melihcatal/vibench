import os
import time
import requests

def poll_transcription_job(job_id: str, polling_interval: int = 10):
    speech_key = os.environ.get("SPEECH_KEY")
    service_region = os.environ.get("SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set.")

    base_url = f"https://{service_region}.api.cognitive.microsoft.com/speechtotext/v3.0"
    transcription_url = f"{base_url}/transcriptions/{job_id}"
    
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
    }

    while True:
        print(f"Polling transcription job {job_id}...")
        response = requests.get(transcription_url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors

        status_data = response.json()
        status = status_data.get("status")
        
        print(f"Job status: {status}")

        if status == "Succeeded":
            print("Transcription job succeeded. Fetching results...")
            # The 'files' link in the response contains a URI to the results manifest
            files_url = status_data.get("links", {}).get("files")
            if files_url:
                files_response = requests.get(files_url, headers=headers)
                files_response.raise_for_status()
                files_data = files_response.json()
                
                # Find the content URL for the transcription result
                for file_item in files_data.get("values", []):
                    if file_item.get("kind") == "Transcription":
                        content_url = file_item.get("links", {}).get("contentUrl")
                        if content_url:
                            print(f"Fetching transcription content from: {content_url}")
                            transcript_response = requests.get(content_url, headers=headers)
                            transcript_response.raise_for_status()
                            
                            # Assuming the content is JSON with 'recognizedPhrases'
                            transcript_json = transcript_response.json()
                            full_transcript = " ".join([phrase.get("nBest", [{}])[0].get("display") 
                                                      for phrase in transcript_json.get("recognizedPhrases", [])])
                            print("Full transcript:")
                            print(full_transcript)
                            return full_transcript
                print("Could not find transcription content URL in the results.")
                return None
            else:
                print("Could not find files link in the transcription job status.")
                return None
        elif status == "Failed":
            print(f"Transcription job failed: {status_data.get('properties', {}).get('error', {}).get('message')}")
            return None
        elif status == "Canceled":
            print("Transcription job was canceled.")
            return None
        
        time.sleep(polling_interval)

if __name__ == "__main__":
    # Example usage: Replace with a real job ID obtained from submitting a batch transcription.
    # This part is illustrative as submitting a job using the REST API is required to get a job ID.
    # For a full example, you would first use the REST API to submit a transcription,
    # which would return a job ID.
    
    # dummy_job_id = "YOUR_TRANSCRIPTION_JOB_ID"
    # os.environ["SPEECH_KEY"] = "YOUR_AZURE_SPEECH_SERVICE_KEY"
    # os.environ["SPEECH_REGION"] = "YOUR_AZURE_SPEECH_SERVICE_REGION"
    
    # if "SPEECH_KEY" in os.environ and "SPEECH_REGION" in os.environ: # and dummy_job_id != "YOUR_TRANSCRIPTION_JOB_ID":
    #     print(f"Attempting to poll job: {dummy_job_id}")
    #     transcript = poll_transcription_job(dummy_job_id)
    #     if transcript:
    #         print(f"Main function received transcript: {transcript}")
    # else:
    #     print("Please set SPEECH_KEY, SPEECH_REGION environment variables and provide a valid job ID.")
    print("To run this example, set SPEECH_KEY, SPEECH_REGION environment variables and uncomment the test lines with a valid job_id.")
