import requests
import time

# Replace with your AssemblyAI API key
# You can get a free API key from https://www.assemblyai.com/
ASSEMBLYAI_API_KEY = "YOUR_ASSEMBLYAI_API_KEY"

# Replace with the URL of your audio file
# Example: "https://storage.googleapis.com/aai-web-samples/5_min_meeting.mp3"
AUDIO_FILE_URL = "YOUR_AUDIO_FILE_URL"

def diarize_audio(audio_url: str, api_key: str):
    """
    Submits an audio file for speaker diarization to AssemblyAI and retrieves the transcript.
    """
    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    # Request a transcript with speaker diarization enabled
    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        json={"audio_url": audio_url, "speaker_diarization": True},
        headers=headers
    )
    response.raise_for_status()
    transcript_id = response.json()["id"]

    # Poll for the transcript to be ready
    while True:
        polling_response = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=headers
        )
        polling_response.raise_for_status()
        status = polling_response.json()["status"]

        if status == "completed":
            return polling_response.json()
        elif status == "error":
            raise Exception(f"AssemblyAI transcription failed: {polling_response.json()['error']}")
        else:
            print(f"Transcript is {status}. Waiting...")
            time.sleep(5)

if __name__ == "__main__":
    if ASSEMBLYAI_API_KEY == "YOUR_ASSEMBLYAI_API_KEY":
        print("Please replace 'YOUR_ASSEMBLYAI_API_KEY' with your actual AssemblyAI API key.")
    elif AUDIO_FILE_URL == "YOUR_AUDIO_FILE_URL":
        print("Please replace 'YOUR_AUDIO_FILE_URL' with the URL of your audio file.")
    else:
        print(f"Starting diarization for {AUDIO_FILE_URL}...")
        try:
            transcript_data = diarize_audio(AUDIO_FILE_URL, ASSEMBLYAI_API_KEY)
            print("\n--- Diarized Transcript ---")
            for utterance in transcript_data["utterances"]:
                print(f"Speaker {utterance['speaker']}: {utterance['text']}")
        except Exception as e:
            print(f"An error occurred: {e}")
