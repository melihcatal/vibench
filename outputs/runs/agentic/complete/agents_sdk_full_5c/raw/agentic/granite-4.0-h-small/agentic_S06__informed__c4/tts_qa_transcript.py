import os
import speech_recognition as sr

# Recognizer setup using Google Cloud Speech-to-Text (other providers possible)
recognizer = sr.Recognizer()

# Helper to read an audio file into raw bytes (used by the TTS pipeline)
import pathlib

def load_audio_bytes(path: str) -> bytes:
    audio_path = pathlib.Path(path)
    with audio_path.open("rb") as f:
        return f.read()


def transcribe_audio(audio_bytes: bytes, provider: str = "google") -> str:
    """Transcribe the synthesized QA sample using the chosen ASR provider."""
    if provider == "google":
        # Use the local speech_recognition wrapper that defaults to Google Cloud.
        with sr.AudioFile(os.path.join("audio", "qa_sample.wav")) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Google Speech Recognition error: {e}"
    else:
        raise NotImplementedError(f"Provider {provider} not implemented")


def check_qa_transcript(tts_output_path: str, reference_text: str) -> bool:
    """
    Transcribe the synthesized QA audio and compare against the expected reference.
    Returns True if transcription contains the reference text (simple substring check).
    """
    audio = load_audio_bytes(tts_output_path)
    transcript = transcribe_audio(audio, provider="google")
    reference_lower = reference_text.lower()
    transcript_lower = transcript.lower()
    match = reference_lower in transcript_lower
    print(f"Reference: {reference_text}\nTranscript: {transcript}\nMatch: {match}")
    return match

# Example usage (script mode)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe synthesized QA audio")
    parser.add_argument("output", help="Path to synthesized .wav file")
    parser.add_argument("reference", help="Expected answer text")
    args = parser.parse_args()
    result = check_qa_transcript(args.output, args.reference)
    print("QA match passed" if result else "QA mismatch detected")
