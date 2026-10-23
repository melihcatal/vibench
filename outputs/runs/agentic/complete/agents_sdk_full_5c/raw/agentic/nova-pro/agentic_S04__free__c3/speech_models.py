class SpeechRequest:
    def __init__(self, audio_file_path, config):
        self.audio_file_path = audio_file_path
        self.config = config

class SpeechResponse:
    def __init__(self, operation):
        self.operation = operation

def normalize_response(response):
    return [alternative.transcript for result in response.results for alternative in result.alternatives]