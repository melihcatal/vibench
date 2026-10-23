import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-cloud-credentials.json"
    client = speech.SpeechClient()

    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    audio_file = "path/to/your/audio_file.wav"
    transcribe_audio(audio_file)