# [SAME-SCENARIO] timestamped_transcript.py
# Returns word/segment timestamps from a transcription result using Azure AI Speech SDK

import os
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY environment variable not set")


def timestamped_transcript(audio_file_path: str) -> str:
    """Transcribes audio and extracts word-level timestamps; returns formatted JSON string.
    Azure Speech SDK provides word-level timestamping via the WordBoundaries feature.
    """
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # Build timestamped output; Azure returns word boundaries in result.get_wrd()
        words = result.get_wrd()  # list of (word, start_time, duration, confidence)
        timestamped = [f"{word[0]}|{word[1]}|{word[2]}" for word in words]
        return "\n".join(timestamped)
    else:
        return "Transcription failed."

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: timestamped_transcript.py <audio_file_path>")
        sys.exit(1)
    ts = timestamped_transcript(sys.argv[1])
    print("Timestamped transcript (word|start|duration):\n")
    print(ts)
