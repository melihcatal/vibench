# [SAME-SCENARIO] timestamped_transcript.py
# Retrieves word-level timestamps from a batch transcription result using Google Cloud Speech-to-Text SDK
import os
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_auth_credentials

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
MODEL = "model=latest_long"


def timestamped_transcript(audio_path: str) -> dict:
    """
    Perform batch transcription with word timestamps using Google Cloud Speech-to-Text.
    Returns the JSON response structured with `results`, each containing `alternatives` with timestamped `words`.
    """
    client = speech.SpeechClient(credentials=get_auth_credentials())
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        use_enhanced=True,
        model=MODEL,
        enable_word_time_offsets=True,
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=300)
    # Normalize results for consistency
    results = []
    for result in response.results:
        alternatives = []
        for alt in result.alternatives:
            words = [
                {
                    "word": word.word,
                    "start": word.start_time.seconds + word.start_time.nanos / 1e9,
                    "end": word.end_time.seconds + word.end_time.nanos / 1e9,
                }
                for word in alt.words
            ]
            alternatives.append(
                {
                    "transcript": alt.transcript,
                    "confidence": alt.confidence,
                    "words": words,
                }
            )
        results.append({"alternatives": alternatives})
    return {"results": results}


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python timestamped_transcript.py <path-to-audio>")
        sys.exit(1)
    transcript = timestamped_transcript(sys.argv[1])
    import json

    print(json.dumps(transcript, indent=2))
