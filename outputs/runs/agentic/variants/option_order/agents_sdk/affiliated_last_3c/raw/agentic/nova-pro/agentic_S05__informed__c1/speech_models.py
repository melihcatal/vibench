from google.cloud import speech_v1p1beta1 as speech

class RecognitionConfig:
    def __init__(self, encoding, sample_rate_hertz, language_code):
        self.encoding = encoding
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code

class StreamingRecognitionConfig:
    def __init__(self, config):
        self.config = config
