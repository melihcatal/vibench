import os
import assemblyai as aai


def transcribe_audio_file(audio_file_path):
    """Transcribe synthesized QA samples to verify spoken output using AssemblyAI."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key

    transcriber = aai.Transcriber()

    try:
        transcript = transcriber.transcribe(audio_file_path)

        return {
            "text": transcript.text,
            "confidence": transcript.confidence,
            "words": [
                {
                    "text": word.text,
                    "start": word.start,
                    "end": word.end,
                    "confidence": word.confidence,
                }
                for word in transcript.words
            ]
            if transcript.words
            else [],
            "duration": transcript.audio_duration,
        }
    except Exception as e:
        raise Exception(f"Transcription failed: {e}")


def transcribe_audio_bytes(audio_bytes):
    """Transcribe audio bytes directly."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key

    config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)

    transcriber = aai.Transcriber()

    try:
        transcript = transcriber.transcribe(data=audio_bytes, config=config)

        return {
            "text": transcript.text,
            "confidence": transcript.confidence,
            "language": transcript.language_code,
            "speakers": transcript.utterances if transcript.utterances else [],
        }
    except Exception as e:
        raise Exception(f"Transcription failed: {e}")
