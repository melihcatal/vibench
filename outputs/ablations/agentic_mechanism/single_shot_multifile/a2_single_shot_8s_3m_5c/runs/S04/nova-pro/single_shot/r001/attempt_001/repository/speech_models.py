class TranscriptionRequest:
    def __init__(self, audio_content):
        self.audio_content = audio_content

class TranscriptionResponse:
    def __init__(self, json_response):
        self.job_id = json_response['name']
        self.status = json_response['metadata']['state']
        self.transcript = json_response['result']['alternatives'][0]['transcript']
        self.timestamped_transcript = json_response['result']['alternatives'][0]['words']