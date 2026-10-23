class TranscriptionRequest:
    def __init__(self, encoding, sample_rate_hertz, language_code, content):
        self.encoding = encoding
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code
        self.content = content

class TranscriptionResponse:
    def __init__(self, job_id):
        self.job_id = job_id

class DiarizationRequest:
    def __init__(self, encoding, sample_rate_hertz, language_code, content, speaker_count):
        self.encoding = encoding
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code
        self.content = content
        self.speaker_count = speaker_count

class DiarizationResponse:
    def __init__(self, diarized_transcript):
        self.diarized_transcript = diarized_transcript

class TimestampedTranscriptRequest:
    def __init__(self, job_id):
        self.job_id = job_id

class TimestampedTranscriptResponse:
    def __init__(self, timestamped_transcript):
        self.timestamped_transcript = timestamped_transcript