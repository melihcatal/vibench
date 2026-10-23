from google.cloud.speech_v1p1beta1 import types

class StreamingConfig:
    def __init__(
        self,
        language_code="en-US",
        sample_rate_hertz=16000,
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        model="latest_long",
        enable_automatic_punctuation=True,
    ):
        self.language_code = language_code
        self.sample_rate_hertz = sample_rate_hertz
        self.encoding = encoding
        self.model = model
        self.enable_automatic_punctuation = enable_automatic_punctuation

    def get_recognition_config(self):
        return types.RecognitionConfig(
            language_code=self.language_code,
            sample_rate_hertz=self.sample_rate_hertz,
            encoding=self.encoding,
            model=self.model,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
        )