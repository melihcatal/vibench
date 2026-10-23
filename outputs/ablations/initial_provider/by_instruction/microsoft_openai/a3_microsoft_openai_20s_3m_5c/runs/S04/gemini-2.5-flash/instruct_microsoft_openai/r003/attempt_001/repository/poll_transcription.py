import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def poll_transcription(transcription_id: str):
    """
    Polls an Azure Speech-to-Text transcription job until it completes and returns the transcript.
    """
    if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
        raise ValueError("Azure Speech key and region must be set in environment variables.")

    url = f"https://{AZURE_SPEECH_REGION}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions/{transcription_id}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY
    }

    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            status_data = response.json()
            status = status_data.get("status")
            
            print(f"Transcription job {transcription_id} status: {status}")

            if status == "Succeeded":
                results_url = status_data["links"]["files"]
                results_response = requests.get(results_url, headers=headers)
                results_response.raise_for_status()
                results_data = results_response.json()
                
                # Find the file that contains the transcript
                for file_data in results_data["values"]:
                    if file_data["kind"] == "Transcription":
                        transcript_url = file_data["links"]["content"]
                        transcript_response = requests.get(transcript_url, headers=headers)
                        transcript_response.raise_for_status()
                        return transcript_response.json()
                return None # Should not happen if status is Succeeded
            elif status in ["Failed", "Canceled"]:
                print(f"Transcription job {transcription_id} failed or was canceled.")
                return None
            else:
                time.sleep(10)  # Wait for 10 seconds before polling again
        except requests.exceptions.RequestException as e:
            print(f"Error polling transcription status: {e}")
            return None

if __name__ == "__main__":
    # Example usage (replace with a valid transcription ID from submit_transcription.py)
    # transcription_job_id = "YOUR_TRANSCRIPTION_ID_HERE"
    # transcript_result = poll_transcription(transcription_job_id)
    # if transcript_result:
    #     print("Transcription successful:")
    #     # The structure of the result can vary, often it's a list of recognized phrases
    #     for utterance in transcript_result.get("recognizedPhrases", []):
    #         print(utterance.get("display"))
    # else:
    #     print("Failed to retrieve transcript.")
    pass
