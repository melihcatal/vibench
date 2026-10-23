class TranscriptRequest:
    def __init__(self, language_code, media_encoding, media_sample_rate, stream_url):
        self.language_code = language_code
        self.media_encoding = media_encoding
        self.media_sample_rate = media_sample_rate
        self.stream_url = stream_url

class TranscriptResponse:
    def __init__(self, transcript_result_stream):
        self.transcript_result_stream = transcript_result_stream