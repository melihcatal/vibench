import os
from google.cloud import speech


def main():
    client = speech.SpeechClient()
    language_code = os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
    sample_rate_hertz = int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE_HZ", "16000"))
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )

    def requests():
        audio_path = os.getenv("GOOGLE_SPEECH_AUDIO_PATH")
        if not audio_path:
            return
        with open(audio_path, "rb") as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

    for response in client.streaming_recognize(streaming_config, requests()):
        for result in response.results:
            if result.alternatives:
                print(result.alternatives[0].transcript)


if __name__ == "__main__":
    main()
