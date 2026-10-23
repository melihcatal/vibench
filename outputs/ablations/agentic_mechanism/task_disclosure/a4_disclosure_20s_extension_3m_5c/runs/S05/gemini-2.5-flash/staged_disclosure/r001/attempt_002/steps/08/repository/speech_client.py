
import os
import google.cloud.speech

class StreamingSpeechClient:
    """
    Provides local configuration and client helper utilities for Streaming Speech-to-Text.
    """
    def __init__(self):
        # Initialize Google Cloud Speech-to-Text client
        self.client = google.cloud.speech.SpeechClient()
        self.config = self._load_config()

    def _load_config(self):
        """
        Loads configuration for speech-to-text.
        In a real application, this would load from a file, environment variables, or a secret manager.
        """
        config = {
            "encoding": google.cloud.speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "sample_rate_hertz": 16000,
            "language_code": "en-US",
            "enable_automatic_punctuation": True,
        }
        return config

    def generate_requests(self, audio_stream):
        """
        Generates streaming recognition requests from an audio stream.
        """
        # The first request contains the recognition config.
        # Subsequent requests contain only the audio data.
        yield google.cloud.speech.StreamingRecognizeRequest(streaming_config=self.streaming_config)

        for chunk in audio_stream:
            yield google.cloud.speech.StreamingRecognizeRequest(audio_content=chunk)

    @property
    def streaming_config(self):
        """
        Returns the streaming recognition configuration.
        """
        return google.cloud.speech.StreamingRecognitionConfig(
            config=google.cloud.speech.RecognitionConfig(
                encoding=self.config["encoding"],
                sample_rate_hertz=self.config["sample_rate_hertz"],
                language_code=self.config["language_code"],
                enable_automatic_punctuation=self.config["enable_automatic_punctuation"],
            ),
            interim_results=True,
        )

# Example usage (would typically be in a separate file or function)
if __name__ == "__main__":
    # This is a placeholder for an actual audio stream, e.g., from a microphone.
    # For demonstration, we'll use a dummy generator.
    def dummy_audio_stream():
        for _ in range(5):
            # Simulate chunks of audio data
            yield b"dummy_audio_chunk"

    speech_client = StreamingSpeechClient()
    print("Speech client initialized with configuration:", speech_client.config)

    # In a real scenario, you would pass an actual audio stream
    # requests = speech_client.generate_requests(dummy_audio_stream())
    # responses = speech_client.client.streaming_recognize(requests)

    # for response in responses:
    #     for result in response.results:
    #         print(f"Transcript: {result.alternatives[0].transcript}")
