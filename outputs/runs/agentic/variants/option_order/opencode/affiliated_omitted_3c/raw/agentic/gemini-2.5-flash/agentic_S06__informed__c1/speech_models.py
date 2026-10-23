class VoiceSelection:
    def __init__(self, name: str = "en-US-JennyNeural", locale: str = "en-US"):
        self.name = name
        self.locale = locale


class AudioOutputConfig:
    def __init__(self, format: str = "Riff24Khz16BitMonoPcm"):
        # See https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech?tabs=streaming#audio-outputs
        self.format = format
