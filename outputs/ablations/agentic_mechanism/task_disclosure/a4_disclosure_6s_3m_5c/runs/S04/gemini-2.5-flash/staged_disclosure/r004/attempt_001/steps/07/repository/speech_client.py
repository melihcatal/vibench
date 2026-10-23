import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

class BatchSpeechToTextClient:
    """
    Client for Google Cloud Batch Speech-to-Text.
    """
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_audio_gcs(self, gcs_uri: str, language_code: str = "en-US", sample_rate_hertz: int = 16000,
                             encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.LINEAR16):
        """
        Transcribes an audio file from a Google Cloud Storage URI using long-running operation.

        Args:
            gcs_uri (str): The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
            language_code (str): The language of the supplied audio (e.g., "en-US").
            sample_rate_hertz (int): The sample rate of the audio file in Hertz.
            encoding (enums.RecognitionConfig.AudioEncoding): The encoding of the audio file.

        Returns:
            google.cloud.speech_v1p1beta1.types.LongRunningRecognizeResponse: The transcription response.
        """

        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="default",  # or "video", "phone_call", "command_and_search"
        )

        operation = self.client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=90)  # Adjust timeout as needed
        return response
