from dataclasses import dataclass


def normalize_text(value):
    return " ".join(str(value).split())


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

    def to_payload(self):
        return {'text': normalize_text(self.text), 'source_language': self.source_language, 'target_language': self.target_language}


@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str

    def to_dict(self):
        return {'text': self.text, 'source_language': self.source_language, 'target_language': self.target_language}


def normalize_segments(segments):
    return [normalize_text(segment) for segment in segments]
