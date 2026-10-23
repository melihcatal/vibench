import os
import assemblyai as aai


def get_assemblyai_client():
    """Initialize and return AssemblyAI client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key
    return aai.Client(api_key=api_key)


def normalize_audio_url(audio_path_or_url):
    """Normalize audio input to URL format."""
    if audio_path_or_url.startswith(("http://", "https://")):
        return audio_path_or_url
    else:
        # For local files, would need to upload first
        # This is a placeholder for actual upload logic
        raise ValueError("Local file upload not implemented. Please provide a URL.")


def parse_transcription_response(transcript):
    """Parse AssemblyAI transcript response to standardized format."""
    if not transcript:
        return None

    result = {
        "id": transcript.id,
        "status": transcript.status.value,
        "text": transcript.text,
        "words": [],
        "utterances": [],
        "confidence": transcript.confidence,
        "audio_duration": transcript.audio_duration,
    }

    if transcript.words:
        result["words"] = [
            {
                "text": word.text,
                "start": word.start,
                "end": word.end,
                "confidence": word.confidence,
            }
            for word in transcript.words
        ]

    if transcript.utterances:
        result["utterances"] = [
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
                "confidence": utterance.confidence,
            }
            for utterance in transcript.utterances
        ]

    return result
