from botocore.response import StreamingBody


class S3Object:
    def __init__(
        self, bucket_name, object_key, content_length, content_type, last_modified
    ):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.content_length = content_length
        self.content_type = content_type
        self.last_modified = last_modified


class PresignedUrl:
    def __init__(self, url, expiration):
        self.url = url
        self.expiration = expiration


class TextractResponse:
    def __init__(self, text, blocks):
        self.text = text
        self.blocks = blocks


class TranslateResponse:
    def __init__(self, translated_text, source_language_code, target_language_code):
        self.translated_text = translated_text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code


class ComprehendResponse:
    def __init__(self, summary, key_phrases):
        self.summary = summary
        self.key_phrases = key_phrases
