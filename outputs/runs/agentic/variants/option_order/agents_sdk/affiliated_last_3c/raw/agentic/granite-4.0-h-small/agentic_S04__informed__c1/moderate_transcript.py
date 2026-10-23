import os
import json
from azure.ai.contentsafety import ContentSafetyClient
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider credentials (env vars or config)
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
MODERATION_CATEGORY = os.getenv('MODERATION_CATEGORY', 'profanity')  # options: \"profanity\", \"hate\", \"selfHarm\", etc.

content_client = ContentSafetyClient(endpoint=AZURE_CONTENT_SAFETY_ENDPOINT, credential=AZURE_CONTENT_SAFETY_KEY)

def moderate_transcript(transcript: str) -> str:
    """Run content safety moderation on transcript and return cleaned version."""
    # Azure Content Safety docs use analyze_content endpoint
    response = content_client.analyze_content(text=transcript, category=MODERATION_CATEGORY)
    # response contains scores and flags; if flag is True, we consider it unsafe
    unsafe = response.unsafe_content_flag
    if unsafe:
        print("Transcript contains unsafe content. Sanitizing...")
        # Simple approach: replace flagged segments with [REDACTED]
        # In production you might use more advanced redaction
        cleaned = \"[REDACTED]\" if MODERATION_CATEGORY == 'profanity' else transcript
        print("Redacted content:", cleaned)
        return cleaned
    else:
        print("Transcript passed moderation.")
        return transcript


def main(file_path: str):
    client = SpeechClient()
    job_id = client.transcribe(file_path, api_key=os.getenv('ASSEMBLYAI_API_KEY'))
    # Use poll_transcription helper from above file
    from poll_transcription import poll_transcription
    segments = poll_transcription(job_id)
    full_transcript = \" \".join([seg['text'] for seg in segments])
    cleaned = moderate_transcript(full_transcript)
    print("Final safe transcript:", cleaned)
    return cleaned

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio, transcribe, then moderate before publishing.")
    parser.add_argument("file", help="Audio file path.")
    args = parser.parse_args()
    moderate_transcript(args.file)
