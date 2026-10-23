class SpeechRequest:
    def __init__(self, audio_file, content_type, model):
        self.audio_file = audio_file
        self.content_type = content_type
        self.model = model


class SpeechResponse:
    def __init__(self, results):
        self.results = results


def normalize_response(response):
    return SpeechResponse(response["results"])
