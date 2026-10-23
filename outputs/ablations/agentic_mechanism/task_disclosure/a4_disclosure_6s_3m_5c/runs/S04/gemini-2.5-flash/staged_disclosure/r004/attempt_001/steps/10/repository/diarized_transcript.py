import assemblyai as aai
import os

# Replace with your AssemblyAI API key
# Get your API key from: https://app.assemblyai.com/
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

# You can also set your API key directly like this:
# aai.settings.api_key = "YOUR_ASSEMBLYAI_API_KEY"

# URL of the audio file to transcribe and diarize
# Replace with your audio file URL or local path
FILE_URL = "https://storage.googleapis.com/aai-web-samples/5_min_meeting.mp3"

transcriber = aai.Transcriber()

config = aai.TranscriptionConfig(
    speaker_diarization=True
)

transcript = transcriber.transcribe(
    FILE_URL,
    config=config
)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print("Diarized Transcript:")
    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
