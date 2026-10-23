import time
import requests
import os

def poll_transcription_job(transcript_id):
    """
    Polls an AssemblyAI transcription job and returns the transcript.
    """
    API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
    if not API_KEY:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }

    while True:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'failed':
            raise Exception(f"Transcription failed: {result.get('error')}")
        else:
            time.sleep(5)  # Wait 5 seconds before polling again

if __name__ == "__main__":
    # Example usage (replace with a real transcript ID and set ASSEMBLYAI_API_KEY env var)
    # transcript_id = "YOUR_TRANSCRIPT_ID"
    # try:
    #     transcript = poll_transcription_job(transcript_id)
    #     print("Transcript:", transcript)
    # except Exception as e:
    #     print("Error:", e)
    pass
