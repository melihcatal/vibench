import assemblyai as aai
import os

# Set your AssemblyAI API key
# You can get one at https://app.assemblyai.com/
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

if not aai.settings.api_key:
    raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

# Initialize the AssemblyAI transcriber
transcriber = aai.Transcriber()

# URL of the audio file to transcribe
# Replace with your actual audio file URL
audio_url = "https://storage.googleapis.com/aai-web-samples/5_9_2024_NYC_call.mp3"

# Configure diarization
config = aai.TranscriptionConfig(speaker_diarization=True)

print(f"Starting transcription and diarization for: {audio_url}")

# Transcribe the audio file with diarization
transcript = transcriber.transcribe(
    audio_url,
    config=config
)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Error: {transcript.error}")
else:
    print("Diarized Transcript:")
    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
