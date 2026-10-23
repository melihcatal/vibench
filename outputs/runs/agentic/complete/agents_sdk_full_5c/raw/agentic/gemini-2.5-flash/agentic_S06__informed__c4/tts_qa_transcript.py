import os
from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_audio_for_qa(audio_filepath: str, language_code: str = "en-US") -> str:
    """Transcribes an audio file using Google Cloud Speech-to-Text for QA verification."""
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(audio_filepath, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000, # Assuming common sample rate for MP3 from TTS
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    print(f"Waiting for operation to complete for {audio_filepath}...")
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=300) # Waits for the operation to complete with a timeout

    transcript = ""
    for result in response.results:
        # The first alternative is the most likely one for transcription
        print(f"Transcript: {result.alternatives[0].transcript}")
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    # Example usage (assuming 'output.mp3' exists from TTS synthesis):
    # audio_file_to_transcribe = "output.mp3"
    # if os.path.exists(audio_file_to_transcribe):
    #     transcribed_text = transcribe_audio_for_qa(audio_file_to_transcribe)
    #     print(f"\nFinal Transcribed Text: {transcribed_text}")
    # else:
    #     print(f"Audio file {audio_file_to_transcribe} not found. Please synthesize audio first.")
    pass
