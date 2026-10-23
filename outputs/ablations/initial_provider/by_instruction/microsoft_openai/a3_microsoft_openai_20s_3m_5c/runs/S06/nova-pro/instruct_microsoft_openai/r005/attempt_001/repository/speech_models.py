class SpeechModels:
    @staticmethod
    def normalize_text(text):
        return text.strip()

    @staticmethod
    def normalize_ssml(ssml):
        return ssml.strip()