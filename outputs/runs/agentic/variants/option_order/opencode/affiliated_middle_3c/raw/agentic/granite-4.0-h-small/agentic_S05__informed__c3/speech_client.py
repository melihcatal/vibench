import os
from google.cloud import speech_v1p1beta1 as speech

# Google Cloud Speech-to-Text client utility
# provider: Cloud Speech-to-Text streaming (service=Cloud Speech streaming)


class SpeechClient:
    """
    Helper client that wraps Google Cloud Speech-to-Text streaming recognition.

    Usage:
        client = SpeechClient()
        stream = client.start_stream(language_code='en-US', punctuation=True)
        for audio_chunk in audio_source():
            stream.send(audio_chunk)
    """

    def __init__(self, credentials_path: str = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = speech.SpeechClient()
        self.config = None
        self.streaming_call = None

    def configure(
        self,
        language_code: str = "en-US",
        enable_automatic_punctuation: bool = True,
        sample_rate_hertz: int = 16000,
    ):
        """
        Prepare streaming config.
        """
        self.config = speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate_hertz,
                language_code=language_code,
                enable_automatic_punctuation=enable_automatic_punctuation,
            ),
            interim_results=True,
        )

    def start_stream(self):
        """
        Begin streaming recognition; returns a bidirectional streaming call.
        Yields:
            dict: transcript event (interim or final)
        """
        if not self.config:
            raise RuntimeError("Call configure() before start_stream()")
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in self._audio_source()
        )
        self.streaming_call = self.client.streaming_recognize(self.config, requests)
        for response in self.streaming_call:
            for result in response.results:
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    is_final = result.is_final
                    yield {"transcript": transcript, "final": is_final}

    def _audio_source(self):
        """Dummy audio generator; replace with real audio stream."""
        with open("sample.wav", "rb") as f:
            while chunk := f.read(4096):
                yield chunk


if __name__ == "__main__":
    client = SpeechClient()
    client.configure()
    stream = client.start_stream()
    for event in stream:
        print(event)
