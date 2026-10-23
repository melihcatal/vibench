from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.oauth2 import service_account

class SpeechToTextClient:
    def __init__(self, credentials_path=None):
        if credentials_path:
            self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = speech.SpeechClient(credentials=self.credentials)
        else:
            self.client = speech.SpeechClient()

    def recognize_batch(self, gcs_uri, language_code="en-US", sample_rate_hertz=16000, enable_automatic_punctuation=True):
        """
        Performs asynchronous speech recognition on an audio file stored in Google Cloud Storage.

        Args:
            gcs_uri (str): The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
            language_code (str): The language of the supplied audio (e.g., "en-US", "es-ES").
            sample_rate_hertz (int): The sample rate in Hertz of the audio data.
            enable_automatic_punctuation (bool): Whether to enable automatic punctuation in the transcription output.

        Returns:
            google.api_core.operation.Operation: An object representing the asynchronous speech recognition operation.
        """

        audio = {"uri": gcs_uri}
        config = {
            "encoding": enums.RecognitionConfig.AudioEncoding.FLAC,  # Assuming FLAC, adjust based on actual audio type
            "sample_rate_hertz": sample_rate_hertz,
            "language_code": language_code,
            "enable_automatic_punctuation": enable_automatic_punctuation,
            "use_enhanced": True,
            "model": "video", # Use appropriate model, e.g., "video", "phone_call", "default"
        }

        operation = self.client.long_running_recognize(config, audio)
        return operation

