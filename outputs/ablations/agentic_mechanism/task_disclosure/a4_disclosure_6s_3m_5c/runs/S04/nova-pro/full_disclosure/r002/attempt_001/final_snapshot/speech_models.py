from google.cloud import speech_v1 as speech

class SpeechRequest:
    def __init__(self, audio_content):
        self.audio_content = audio_content

    def to_dict(self):
        return {
            'config': {
                'encoding': 'LINEAR16',
                'sample_rate_hertz': 16000,
                'language_code': 'en-US',
            },
            'audio': {
                'content': self.audio_content,
            }
        }

class SpeechResponse:
    def __init__(self, response):
        self.response = response

    def to_text(self):
        return ' '.join([result.alternatives[0].transcript for result in self.response.results])

def normalize_transcript(transcript):
    return transcript.lower().strip()