class SynthesizeTextRequest:
    def __init__(self, text: str, voice_name: str = 'en-US-JennyNeural'):
        self.text = text
        self.voice_name = voice_name

class SynthesizeSsmlRequest:
    def __init__(self, ssml: str):
        self.ssml = ssml

class SelectVoiceRequest:
    def __init__(self, locale: str = 'en-US'):
        self.locale = locale

class AudioSaveRequest:
    def __init__(self, audio_bytes: bytes, file_path: str, s3_bucket_name: str = None, aws_access_key_id: str = None, aws_secret_access_key: str = None, aws_region: str = None):
        self.audio_bytes = audio_bytes
        self.file_path = file_path
        self.s3_bucket_name = s3_bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

class SynthesizeResponse:
    def __init__(self, audio_bytes: bytes, content_type: str):
        self.audio_bytes = audio_bytes
        self.content_type = content_type

class SelectVoiceResponse:
    def __init__(self, voices: list):
        self.voices = voices

class AudioSaveResponse:
    def __init__(self, status: str, location: str):
        self.status = status
        self.location = location