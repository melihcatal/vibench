class TranscriptionRequest:
    def __init__(self, config, audio):
        self.config = config
        self.audio = audio

class TranscriptionResponse:
    def __init__(self, results):
        self.results = results

def normalize_transcription_response(response):
    results = response['results']
    normalized_results = [{'alternatives': [alt['transcript'] for alt in res['alternatives']]} for res in results]
    return TranscriptionResponse(normalized_results)