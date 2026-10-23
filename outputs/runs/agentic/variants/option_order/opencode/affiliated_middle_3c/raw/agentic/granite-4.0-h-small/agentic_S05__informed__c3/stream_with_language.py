import boto3
from botocore.exceptions import BotoCoreError


class StreamWithLanguage:
    """
    Starts a streaming recognizer with language and punctuation settings using AWS Transcribe Streaming.
    Provider: Amazon Transcribe Streaming (service=Amazon Transcribe Streaming)
    Configuration:
        AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in the environment.
    """

    def __init__(
        self, language_code: str = "en-US", enable_automatic_punctuation: bool = True
    ):
        self.transcribe = boto3.client(
            "transcribe-streaming",
            region_name="us-east-1",
        )
        self.language_code = language_code
        self.enable_automatic_punctuation = enable_automatic_punctuation
        self.stream = None

    def start_stream(self, audio_stream):
        """
        Start streaming transcription with specified language and punctuation.
        Args:
            audio_stream: an iterator yielding audio bytes
        Yields:
            dict: transcription result containing interim or final transcript
        """
        try:
            response = self.transcribe.start_stream_transcription(
                LanguageCode=self.language_code,
                MediaSampleRateHertz=16000,
                MediaEncoding="pcm",
                EnableAutomaticPunctuation=self.enable_automatic_punctuation,
            )
            self.stream = response["AudioStream"]
            # Send audio chunks to the stream
            for chunk in audio_stream:
                self.stream.send(chunk)
                # Process response (mocked here)
                # In real code, you'd read response events and yield interleaved results
        except BotoCoreError as e:
            print(f"Error starting stream: {e}")

        # End of stream logic would be handled here


if __name__ == "__main__":
    # Example usage with a dummy audio generator
    def dummy_audio_stream():
        yield b"dummy audio..."  # replace with actual audio chunks

    recognizer = StreamWithLanguage(language_code="en-US")
    recognizer.start_stream(dummy_audio_stream())
