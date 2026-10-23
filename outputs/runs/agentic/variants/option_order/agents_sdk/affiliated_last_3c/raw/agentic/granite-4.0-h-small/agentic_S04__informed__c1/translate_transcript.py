import os
import json
from google.cloud import translate_v2 as translate
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider credentials (env vars or config)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TRANSLATE_TARGET = os.getenv('TRANSLATE_TARGET', 'es')  # default Spanish

# Initialize Cloud Translation client
translate_client = translate.Client()

def translate_transcript(transcript: str) -> str:
    """Translate provided transcript text into target language."""
    # Use Google Cloud Translation API (SDK)
    result = translate_client.translate(transcript, target_language=TRANSLATE_TARGET)
    return result['translatedText']


def main(file_path: str):
    client = SpeechClient()
    job_id = client.transcribe(file_path, api_key=os.getenv('ASSEMBLYAI_API_KEY'))
    # Assume poll_transcription from poll_transcription.py exists in same module
    from poll_transcription import poll_transcription
    segments = poll_transcription(job_id)
    # Concatenate segments into full transcript string
    full_transcript = \" \".join([seg['text'] for seg in segments])
    translated = translate_transcript(full_transcript)
    print("Translated transcript:")
    print(translated)
    return translated

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio, get transcription, then translate.")
    parser.add_argument("file", help="Path to audio file.")
    args = parser.parse_args()
    translate_transcript(args.file)
