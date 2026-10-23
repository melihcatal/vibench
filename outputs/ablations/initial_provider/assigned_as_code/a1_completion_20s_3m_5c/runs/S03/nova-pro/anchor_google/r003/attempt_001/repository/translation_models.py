class TranslationRequest:
    def __init__(self, text, source_language, target_language, mime_type='text/plain'):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language
        self.mime_type = mime_type

    def to_dict(self):
        return {
            'text': self.text,
            'source_language': self.source_language,
            'target_language': self.target_language,
            'mime_type': self.mime_type,
        }


class TranslationResponse:
    def __init__(self, translated_text, source_language, target_language):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

    @classmethod
    def from_dict(cls, data):
        return cls(
            translated_text=data['translated_text'][0],
            source_language=data['source_language'],
            target_language=data['target_language'],
        )

    def to_dict(self):
        return {
            'translated_text': self.translated_text,
            'source_language': self.source_language,
            'target_language': self.target_language,
        }