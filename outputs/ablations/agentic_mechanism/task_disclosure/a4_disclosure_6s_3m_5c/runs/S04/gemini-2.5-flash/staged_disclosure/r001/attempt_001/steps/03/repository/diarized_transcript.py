
import os
import assemblyai as aai

def diarize_audio(audio_url):
    """
    Transcribes an audio file and performs speaker diarization using AssemblyAI.

    Args:
        audio_url (str): The URL of the audio file to diarize.

    Returns:
        aai.Transcript: The transcript object with diarization information.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    config = aai.TranscriptionConfig(speaker_labels=True)

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"AssemblyAI transcription error: {transcript.error}")

    return transcript

if __name__ == "__main__":
    # Replace with your audio file URL
    audio_file_url = "https://storage.googleapis.com/aai-web-samples/5_min_meeting.mp3"

    try:
        print(f"Starting diarization for {audio_file_url}...")
        diarized_result = diarize_audio(audio_file_url)

        print("\nTranscription with Speaker Diarization:")
        for utterance in diarized_result.utterances:
            print(f"Speaker {utterance.speaker}: {utterance.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
