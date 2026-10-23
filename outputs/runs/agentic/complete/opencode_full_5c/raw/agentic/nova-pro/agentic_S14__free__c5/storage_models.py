class S3Object:
    def __init__(self, bucket_name, key):
        self.bucket_name = bucket_name
        self.key = key


class TextractResponse:
    def __init__(self, text):
        self.text = text


class TranslateResponse:
    def __init__(self, translated_text):
        self.translated_text = translated_text


class ComprehendResponse:
    def __init__(self, summary):
        self.summary = summary
