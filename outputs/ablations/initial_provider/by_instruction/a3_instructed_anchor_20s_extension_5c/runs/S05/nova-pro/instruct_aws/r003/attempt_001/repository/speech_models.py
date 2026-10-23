class SpeechRequest:
    def __init__(self, language_code='en-US'):
        self.language_code = language_code

    def to_dict(self):
        return {
            'LanguageCode': self.language_code,
            'Media': {
                'MediaFileUri': 's3://your-bucket/your-audio-file'
            }
        }

class SpeechResponse:
    def __init__(self, results):
        self.results = results

    def normalize(self):
        return [result['Alternatives'][0]['Transcript'] for result in self.results]